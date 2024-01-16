def get_subj_numbers():
    # Subject names
    subjInput = input("Enter subject number (99 for all subj, 91 to start from a subj to all): ")
    subj_number = int(subjInput)

    # if the input is 99, then compute on all subjects
    if subj_number == 99:
        subj_number = [2,3,5,6,7,8,9,10,11,12,13,14,15,16,17,19,20,21,22,23,24,26,27,28,29,30]
    elif subj_number == 91:
        subjInputR = input("Start from which subject?: ") #camel R stands for range
        subj_number = range(int(subjInputR), 31)
        print("Working on: " + str(subj_number))
    else:
        subj_number = [int(subjInput)]

    return subj_number

