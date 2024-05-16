{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#!pip install ipynb"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "from ipynb.fs.full.fail_stop_agreement import agreement, Process\n",
    "import threading\n",
    "\n",
    "n = 4"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def run_protocol(processes):\n",
    "    threads = []\n",
    "\n",
    "    for i in range(0, n):\n",
    "        thr = threading.Thread(target=agreement, args=((processes[i],)))\n",
    "        threads.append(thr)\n",
    "    \n",
    "    for thr in threads:    \n",
    "        thr.start()\n",
    "\n",
    "    for thr in threads:\n",
    "        thr.join()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def test_same_input(input):\n",
    "    processes = []\n",
    "\n",
    "    for i in range(0, n):\n",
    "        pr = Process(i, input)\n",
    "        processes.append(pr)\n",
    "\n",
    "    run_protocol(processes)\n",
    "\n",
    "    print(\"*******   SOLUTION:   *******\")\n",
    "    for pr in processes:\n",
    "        print(\"process(\", pr.id, \") = \", pr.output, \" @epoch: \", pr.decision_epoch)\n",
    "        if pr.output != input or pr.decision_epoch != 1:\n",
    "            return False\n",
    "    print(\"-----------------------------\")\n",
    "    return True"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Lemma 9\n",
    "During each epoch, both of the values 0 and 1 are never sent in any execution of round 2"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_round2_msgs(processes):\n",
    "    epochs_num = [pr.decision_epoch+1 for pr in processes]\n",
    "    total_epochs = max(epochs_num)\n",
    "    \n",
    "    round2_msgs_per_epoch = [[]] * total_epochs\n",
    "\n",
    "    for pr in processes:\n",
    "        for msg in pr.broadcasted_messages:\n",
    "            if msg.round == 2:\n",
    "                round2_msgs_per_epoch[msg.epoch-1].append(msg.message)      # epoch numbers start at 1 but list positions start at 0\n",
    "    return round2_msgs_per_epoch\n",
    "\n",
    "def test_lemma_9():\n",
    "    processes = []\n",
    "\n",
    "    for i in range(0, n):\n",
    "        pr = Process(i, str(i%2))\n",
    "        processes.append(pr)\n",
    "\n",
    "    run_protocol(processes)\n",
    "\n",
    "    # Pre-processing: get all round 2 messages per epoch\n",
    "    round2_msgs_per_epoch = get_round2_msgs(processes)\n",
    "    \n",
    "    for epoch_msgs in round2_msgs_per_epoch:\n",
    "        print(epoch_msgs)\n",
    "        ocurrences_0 = epoch_msgs.count(\"0\")\n",
    "        ocurrences_1 = epoch_msgs.count(\"1\")\n",
    "        if ocurrences_0 > 0 and ocurrences_1 > 0:\n",
    "            return False\n",
    "    return True"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Agreement: Let e be the first epoch in which a processor decides. If processor P decides v in epoch e, then by the end of epoch e + 1 all processors decide v. "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def test_agreement():\n",
    "    first_decision_epoch = None\n",
    "    first_value = None\n",
    "    for pr in processes:\n",
    "        if pr.id == first_to_decide:\n",
    "            first_decision_epoch = pr.decision_epoch\n",
    "            first_value = pr.output\n",
    "            break\n",
    "    \n",
    "    for pr in processes:\n",
    "        if (pr.decision_epoch != first_decision_epoch and pr.decision_epoch !=  first_decision_epoch+1) or pr.output != first_value:\n",
    "            return False\n",
    "    return True"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "def test_all():\n",
    "    #print(test_same_input(\"0\"))\n",
    "    #print(test_same_input(\"1\"))\n",
    "    print(test_lemma_9())\n",
    "\n",
    "test_all()"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": ".venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}