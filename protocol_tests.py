def test_validity(processes):
    inputs = []
    for pr in processes:
        inputs.append(pr.input_val)
    assert(len(inputs) > 0)
    common_val = inputs[0]
    same_input = all(val == common_val for val in inputs)
    
    if same_input:
        for pr in processes:
            if pr.output != common_val or pr.decision_epoch != 1:
                return False
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

# Termination: all non faulty processes decide upon a value with probability 1
def test_termination(processes):
    for pr in processes:
        if pr.non_faulty and pr.output == None:
            return False
    return True

def test_all(processes, first_to_decide):
    lemma_9 = test_lemma_9(processes)
    agreement = test_agreement(processes, first_to_decide)
    termination = test_termination(processes)
    validity = test_validity(processes)
    tests = [lemma_9, agreement, termination, validity]

    print("PASSED TESTS: ", tests.count(True), "/", len(tests))
    print("Lemma 9: ", lemma_9)
    print("Agreement: ", agreement)
    print("Termination: ", termination)
    print("Validity: ", validity)
    print()