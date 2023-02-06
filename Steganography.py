import cv2
import numpy as np

def displayData(img):
    b_data = ""
    for val in img:
        for px in val:
            r,g,b = toBinary(px)
            # extract the least significant bit from each 
            # rgb binary colour. 
            b_data += r[-1]
            b_data += g[-1]
            b_data += b[-1]
    # split by 8-bits
    all_bytes = [b_data[i:i+8] for i in range(0,len(b_data),8)]
    # convert bits to chars
    decoded_text = ""
    for b in all_bytes:
        decoded_text += chr(int(b,2))
        # check to reach the delimiter 
        if decoded_text[-5:] == "#####": 
            break
    
    return decoded_text[:-5]
'''
Controller function to decode text from the img 
'''
def decoded_data():
    img_name = input("Enter the name of img you want to decode (with .png extension): ")
    img = cv2.imread(img_name)

    #show the text
    text = displayData(img)
    return text
'''
Convert any data type to binary 
'''
def toBinary(messg):
    if type(messg) == str:
        return ''.join([format(ord(i), "08b") for i in messg])
    elif type(messg) == bytes or type(messg) == np.ndarray:
        return [format(i,"08b") for i in messg]
    elif type(messg) == int or type(messg) == np.uint8:
        return format(messg, "08b")
    else:
        raise TypeError("Input type not supported")
'''
Hide the secret text into the binary of the image
'''
def hide_data(img, messg):
    #Max bytes to encode
    n_bytes = img.shape[0] * img.shape[1] * 3 // 8
    #check if the number of bytes to encode are less than the bytes in the image
    if len(messg) > n_bytes:
        raise ValueError("Error size of img is too small or the message is too large")

    messg += "#####"

    data_index = 0
    #binary_message
    b_message = toBinary(messg=messg)
    data_len = len(b_message)
    for val in img:
        for px in val:
            # convt rgb to binary
            r,g,b = toBinary(px)

            if data_index < data_len:
                #hide the data into the least significant bit of red pixel
                px[0] = int(r[:-1]+b_message[data_index], 2)
                data_index += 1
            if data_index < data_len:
                #hide the data into the least significant bit of green pixel
                px[1] = int(g[:-1]+b_message[data_index], 2)
                data_index += 1
            if data_index < data_len:
                #hide the data into the least significant bit of blue pixel
                px[2] = int(b[:-1]+b_message[data_index], 2)
                data_index += 1
            if data_index >= data_len:
                break
    return

'''
Encode data into the image 
'''
def encode_data():
    img_name = input("Enter image name (with .png extension): ")
    img = cv2.imread(img_name)
    print("shape of img: ", img.shape)
    data = input("Enter data to be encoded: ")
    if len(data) != 0:
        filename = input("Enter the name of the new encoded image(with .png extension): ")
        ## make encoded image and save the image 
        hide_data(img, data)
        cv2.imwrite(filename, img)
    return 

'''
This is the controller function
'''
def Steganography():
    i = input("Image \n 1. Encode data \n 2. Decode data \n Your input: ")
    user_answer = int(i)
    if user_answer == 1:
        print("\nEncoding ...")
        encode_data()
    elif user_answer == 2:
        print("\nDecoding ...")
        text = decoded_data()
        print("Decoded message is: " + text)
    else:
        print("\n Invalid input")
    return 

Steganography() #main function call 