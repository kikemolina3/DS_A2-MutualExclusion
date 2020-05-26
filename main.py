#! /usr/bin/python3
from cos_backend import COSBackend
import pywren_ibm_cloud as pywren
from sys import argv
import time, json

X = 0.05

# Master function: controls mutual exclusion in 'result.json' writes. 
# It gives permission to write according to creation date
def master(x, ibm_cos):  
    obj = COSBackend(config=ibm_cos)
    def order(e):
        return e['LastModified']
    write_permission_list = []  
    m = []
    finish = 0
    obj.put_object('practise2', 'result.json', json.dumps(m))
    l = obj.list_objects('practise2', 'p_write')
    while (not finish): 
        l.sort(key=order) 
        current_id = l.pop(0)
        current_id = current_id['Key']
        file_to_write = current_id[2:]
        date_json = obj.list_objects('practise2', 'result.json')[0]['LastModified']
        obj.put_object('practise2', file_to_write, "")
        obj.delete_object('practise2', "p_" + file_to_write) 
        write_permission_list.append(int(file_to_write[7:-1]))
        next = 0
        while (not next):
            time.sleep(X/4)
            if (not obj.list_objects('practise2', 'result.json')[0]['LastModified'] == date_json):
                next = 1
        obj.delete_object('practise2', file_to_write) 
        time.sleep(X)
        l = obj.list_objects('practise2', 'p_write')
        if (not l):
            finish = 1
    return write_permission_list 

# Slave function: when has permissions append its identifier to 'result.json'
def slave(id, x, ibm_cos): 
    obj = COSBackend(config=ibm_cos)
    obj.put_object('practise2', "p_write_{" + str(id) + "}", b"")
    my_turn = 0
    while (not my_turn):
        time.sleep(X)
        if (obj.list_objects('practise2', 'write_{' + str(id) + '}')):
            my_turn = 1
    result_file = json.loads(obj.get_object('practise2', 'result.json'))
    result_file.append(id)
    obj.put_object('practise2', 'result.json', json.dumps(result_file))

if __name__ == '__main__':
    n_slaves = int(argv[1])
    if n_slaves < 1 or n_slaves > 256:
        print("Slaves' number must be between 1-256")
        exit()
    # Executor's creation
    pw = pywren.ibm_cf_executor()
    ibm_cos = pw.internal_storage.get_client()
    # Master & slave's calls
    start = time.time()
    pw.map(slave, range(n_slaves))
    pw.call_async(master, 0)  
    # Result's comparation
    write_permission_list = pw.get_result()
    end = time.time() - start
    print("Ex. time=\t" + str(end))
    write_order = json.loads(ibm_cos.get_object(Bucket='practise2', Key='result.json')['Body'].read())
    print("Write order=\t" + str(write_order) + "\nPermision order=" + str(write_permission_list))
    print("Success!" if write_permission_list == write_order else "Failure!")