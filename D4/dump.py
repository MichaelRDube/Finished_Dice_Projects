from ultralytics import YOLO
import shutil
import cv2
import os
import sqlite3

#load the trained YOLOv8 model
model = YOLO('./models/D4_Identifier.pt')

#Directory containing the images to process
test_folder = './captured_images'

def save_to_database(inserts):
    try:
        conn = sqlite3.connect('dice.db')

        cursor = conn.cursor()
        cursor.executemany(
        '''
        insert into rolls(path, label, confidence, flagged)
        values(?, ?, ?, ?)
        ''',
        inserts
        )
    except:
        print("Could not add rolls to database.")
    finally:
        conn.commit()
        conn.close()

def sets_match(set1, set2):
    print("Comparing:")
    print(set1)
    print("Against known set:")
    print(set2)

    for item in set1:
        if item not in set2:
            print("Not a match")
            print()
            return False
    for item in set2:
        if item not in set1:
            print("Not a match")
            print()
            return False
        
    print("Match found")
    print()
    return True

def process_images(image_dir):
    inserts = []
    
    image_list = os.listdir(image_dir)
    image_list.sort()

    # Iterate over images in the directory
    for img_name in image_list:
        if img_name.endswith('.jpg') or img_name.endswith('.png'):
            img_path = os.path.join(image_dir, img_name)
            img = cv2.imread(img_path)

            # Specify the scaling factor
            pic_width = 900
            ratio = pic_width/img.shape[1]
            pic_height = int(ratio*img.shape[0])  # Scale down to 50% of original height

            # Calculate the new size
            new_size = (pic_width, pic_height)

            # Resize the image
            img = cv2.resize(img, new_size)

            cv2.imshow('Image Preview', img)
            cv2.waitKey(1)

            results = model(img)

            min_conf = 100
            digits_found = []

            for result in results:
                for bbox in result.boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, bbox.xyxy[0])
                    width, height = x2 - x1, y2 - y1
                    # Check if any results are detected
                    if len(results) > 0:
                        # Get object label and confidence for each bounding box
                        object_label = result.names[bbox.cls.item()]  # Get the label for the current bounding box
                        confidence = bbox.conf.item()  # Confidence score for the current bounding box
                        confidence_percentage = round(confidence * 100, 2)  # Convert to percentage

                        label_with_confidence = f"{object_label} {confidence_percentage}%"
                        
                        # Draw the bounding box on the original image
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, label_with_confidence, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

                        if confidence_percentage < min_conf:
                            min_conf = confidence_percentage

                        digits_found.append(object_label)
                    else:
                        # Handle cases where no objects are classified
                        print(f"No objects detected in cropped image {img}")

            if min_conf < 80:
                flag = True
                print('Low confidence identification: ' + str(min_conf) + '%.  Flagging.')
            else:
                flag = False

            if len(digits_found) == 1:
                if digits_found[0] == 'max':
                    object_label = 1
                else:
                    print('One digit found, not max.  Flagging.')
                    flag = True
                    object_label = 0
            elif len(digits_found) != 3:
                print("Incorrect number of digits found.  Flagging.")
                flag = True
                object_label = 0
            else:
                if sets_match(digits_found, ['1', '2', '3']):
                    object_label = 4
                elif sets_match(digits_found, ['1', '2', '4']):
                    object_label = 3
                elif sets_match(digits_found, ['1', '3', '4']):
                    object_label = 2
                else:
                    print("Digits found do not match any valid sets.  Flagging.")
                    flag = True
                    object_label = 0

            inserts.append((os.path.join('processed_images', img_name), object_label, min_conf, flag))
            print("Appended " + str(object_label) + " with confidence " + str(confidence_percentage) + ", flag: " + str(flag))

            # Show the image with boxes and labels
            cv2.imshow('Image Preview', img)
            cv2.waitKey(1)

    #move files from captured_images to processed_images
    for file in os.listdir('./captured_images'):
        shutil.move(os.path.join('./captured_images', file), './processed_images')
    #print(inserts)
    save_to_database(inserts)


    flag_count = 0
    flagged_digits = []
    print()
    print('Flagged items:')
    for roll in inserts:
        if roll[3]:
            flag_count += 1
            print(roll[0])
            if roll[1] not in flagged_digits:
                flagged_digits.append(roll[1])

    if flag_count == 0:
        print("None")
    else:
        print("Total flagged items:  " + str(flag_count))
        print(f'Misidentified Digits:  {flagged_digits}')


    cv2.destroyAllWindows()

# Run the function
process_images('captured_images')
