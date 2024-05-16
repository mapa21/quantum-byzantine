import threading
#from fail_stop_agreement import agreement, Process, processes, first_to_decide, n

def agreement():
    pass
class Process:
    pass

n = None

def run_protocol(processes):
    threads = []

    for i in range(0, n):
        thr = threading.Thread(target=agreement, args=((processes[i],)))
        threads.append(thr)
    
    for thr in threads:    
        thr.start()

    for thr in threads:
        thr.join()
def test_same_input(input):
    processes = []

    for i in range(0, n):
        pr = Process(i, input)
        processes.append(pr)

    run_protocol(processes)

    print("*******   SOLUTION:   *******")
    for pr in processes:
        print("process(", pr.id, ") = ", pr.output, " @epoch: ", pr.decision_epoch)
        if pr.output != input or pr.decision_epoch != 1:
            return False
    print("-----------------------------")
    return True

# Lemma 9
# During each epoch, both of the values 0 and 1 are never sent in any execution of round 2

def get_round2_msgs(processes):
    epochs_num = [pr.decision_epoch+1 for pr in processes]
    total_epochs = max(epochs_num)
    
    round2_msgs_per_epoch = [[]] * total_epochs

    for pr in processes:
        for msg in pr.broadcasted_messages:
            if msg.round == 2:
                round2_msgs_per_epoch[msg.epoch-1].append(msg.message)      # epoch numbers start at 1 but list positions start at 0
    return round2_msgs_per_epoch

def test_lemma_9(processes):
    # Pre-processing: get all round 2 messages per epoch
    round2_msgs_per_epoch = get_round2_msgs(processes)
    
    for epoch_msgs in round2_msgs_per_epoch:
        ocurrences_0 = epoch_msgs.count("0")
        ocurrences_1 = epoch_msgs.count("1")
        if ocurrences_0 > 0 and ocurrences_1 > 0:
            return False
    return True
# Agreement: Let e be the first epoch in which a processor decides. If processor P decides v in epoch e, 
 #           then by the end of epoch e + 1 all processors decide v.

def test_agreement(processes, first_to_decide):
    first_decision_epoch = None
    first_value = None
    for pr in processes:
        if pr.id == first_to_decide:
            first_decision_epoch = pr.decision_epoch
            first_value = pr.output
            break
    
    for pr in processes:
        if (pr.decision_epoch != first_decision_epoch and pr.decision_epoch !=  first_decision_epoch+1) or pr.output != first_value:
            return False
    assert(first_decision_epoch is not None)
    return True

def test_all(processes, first_to_decide):
    #print(test_same_input("0"))
    #print(test_same_input("1"))
    print("Lemma 9: ", test_lemma_9(processes))
    print("Agreement property: ", test_agreement(processes, first_to_decide))