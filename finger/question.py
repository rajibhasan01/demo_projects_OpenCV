import random
import cv2
import time


countdown = 0;
status = None;
counter_start = time.time();
question = random.randint(0,4);
final_result_for_all_qstn = [];
buffer_result_for_single_qstn = [];


# Generating new question
def generate_qstn(img):
    global question;
    global countdown;
    global counter_start;
    current_time = time.time()
    time_counter = generate_timer(current_time);
    
    if counter_start + 3 < current_time:
        new_question = random.randint(1,4);
        if question == new_question:
            if question == 1:
                new_question = question + 1;
            else:
                new_question = question -1;
                
        counter_start = current_time;
        countdown = 0;
        question = new_question;
        
        # calculate previous question answer
        if status == None:
            calculate_result();
    
    # check status
    if status != None:
        display_result(img);
       
    else:
        display_question(img, question, time_counter);
        return question;


#Edit image frame with question
def display_question(img, question, timer):
    
    text = "Show Finger " + str(question);
    cv2.rectangle(img, (170, 10), (440, 50), (0, 255, 0), cv2.FILLED);
    cv2.putText(img,f'Timer: {timer}',(510,35),cv2.FONT_HERSHEY_COMPLEX,0.7,(0, 65, 255),1);
    cv2.putText(img,text,(180,40),cv2.FONT_HERSHEY_COMPLEX,1,(255, 0, 0),2);
    return img;

# Edit image frame with result
def display_result(img):
    global status;
    if status == "Verified":
        bg = (106, 176, 76);
        txt_position = (240,40)
    else:
        bg = (0, 0, 205);
        txt_position = (220,40);
    cv2.rectangle(img, (170, 10), (440, 50), bg, cv2.FILLED);
    cv2.putText(img, status,txt_position,cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2);
    return img;
    

# Check match for every buffering question
def match_q_a(img, given_finger_count, asked_finger_count):
    
    global buffer_result_for_single_qstn;
    global counter_start;
    
    if given_finger_count == asked_finger_count:
        buffer_result_for_single_qstn.append(1);
    else:
        buffer_result_for_single_qstn.append(0);
    

# Generating countdown for each question
def generate_timer(current_time):
    
    global countdown;
    global counter_start;
    
    if  counter_start + 1 < current_time:
        countdown += 1;
        return countdown;
    else:
        return countdown;


# Result Calculation
def calculate_result():
    
    global final_result_for_all_qstn;
    global buffer_result_for_single_qstn;
    
    total_buffer_count = len(buffer_result_for_single_qstn);
    total_buffer_true_value_count = buffer_result_for_single_qstn.count(1);
    
    try:
        true_value_percentage = (total_buffer_true_value_count / total_buffer_count) * 100;
    except:
        true_value_percentage = 0;
        
    if true_value_percentage > 50:
        final_result_for_all_qstn.append(1);
        print("true");
    else:
        final_result_for_all_qstn.append(0);
        print("false");
    
    buffer_result_for_single_qstn.clear();
    
    if len(final_result_for_all_qstn) == 4:
        make_decision(final_result_for_all_qstn);
        final_result_for_all_qstn.clear();
        print(final_result_for_all_qstn);


# Make a decision for varified or not
def make_decision(final_result_for_all_qstn):
    
    global status;
    rignt_ans_count = final_result_for_all_qstn.count(1);
    
    if(rignt_ans_count >= 3):
        status = "Verified"
        print("Passed")
    else:
        status = "Unverified"
        print("failed")