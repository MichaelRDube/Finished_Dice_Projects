from ultralytics import YOLO
import shutil
import cv2
import os
import sqlite3

die_max = 12
confidence_thresholds = [75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75, 75]
#rolls:                  1   2   3   4   5   6   7   8   9   10  11  12

# Load the two models
print("Loading digit finder...")
model_stage1 = YOLO('./models/Digit_Model.pt')  # Object detection model
print("Loading digit identifier...")
model_stage2 = YOLO('./models/Digit_Identifier_Model.pt')  # Object classification model

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


def process_images(image_dir, save_cropped_dir='temp_crops'):
    inserts = []
    # Ensure the directory for temporary cropped images exists
    os.makedirs(save_cropped_dir, exist_ok=True)
    
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

            # First stage: Detect objects
            results_stage1 = model_stage1(img)

            firstlook = True
            for i, result in enumerate(results_stage1):

                for bbox in result.boxes:

                    if firstlook:
                        print("New digit found.")
                        firstlook = False
                    else:
                        print("Skipping duplicate image.")
                        break

                    # Get bounding box coordinates
                    x1, y1, x2, y2 = map(int, bbox.xyxy[0])
                    width, height = x2 - x1, y2 - y1
                    
                    # Calculate new dimensions for cropping with object roughly 70% of the image
                    expand_factor = 1.4286  # Expands the crop to be larger than the bounding box
                    crop_x1 = max(0, int(x1 - width * (expand_factor - 1) / 2))
                    crop_y1 = max(0, int(y1 - height * (expand_factor - 1) / 2))
                    crop_x2 = min(img.shape[1], int(x2 + width * (expand_factor - 1) / 2))
                    crop_y2 = min(img.shape[0], int(y2 + height * (expand_factor - 1) / 2))
                    
                    # Crop the image
                    cropped_img = img[crop_y1:crop_y2, crop_x1:crop_x2]

                    # Save temporary cropped image
                    cropped_img_path = os.path.join(save_cropped_dir, f'crop_{img_name}_{i}.jpg')
                    cv2.imwrite(cropped_img_path, cropped_img)

                    # Second stage: Classify cropped object
                    results_stage2 = model_stage2(cropped_img)
                    # Check if any results are detected
                    if len(results_stage2) > 0 and len(results_stage2[0].boxes.cls) > 0:
                        object_label = results_stage2[0].names[results_stage2[0].boxes.cls[0].item()]
                        confidence = results_stage2[0].boxes.conf[0].item()  # Confidence score of the first detected object
                        confidence_percentage = round(confidence * 100, 2)  # Convert to percentage

                        label_with_confidence = f"{object_label} {confidence_percentage}%"
                        
                        # Draw the bounding box on the original image
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(img, label_with_confidence, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

                        try:
                            #convert max rolls to integer of die max
                            max_roll = False
                            if object_label == 'max':
                                object_label = die_max
                                max_roll = True
                            else:
                                object_label = int(object_label)

                            if object_label >= die_max and not max_roll:
                                flag = True
                                object_label = 0
                                print("Roll misidentified.  Flagging and assigning value 0.")
                            elif confidence_percentage < confidence_thresholds[object_label-1]:
                                flag = True
                            else:
                                flag = False

                            inserts.append((os.path.join('processed_images', img_name), object_label, confidence_percentage, flag))
                            print("Appended " + str(object_label) + " with confidence " + str(confidence_percentage) + ", flag: " + str(flag))

                        except:
                            print('Something went wrong with identification.')
                    else:
                        # Handle cases where no objects are classified
                        print(f"No objects detected in cropped image {cropped_img_path}")
                    
            # Show the image with boxes and labels
            cv2.imshow('Image Preview', img)
            cv2.waitKey(1)

            for file in os.listdir(save_cropped_dir):
                if os.path.isfile(os.path.join(save_cropped_dir, file)):
                    os.remove(os.path.join(save_cropped_dir, file))

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
process_images('./captured_images')

