class Rtype:
    id = None
    type = None
    rs = None
    rt = None
    rd = None

    def __init__(self, id, type, rs, rt, rd):
        self.id = id
        self.type = type
        self.rs = rs
        self.rt = rt
        self.rd = rd

    def __str__(self):
        return  self.type + " "+self.rd+",  "+self.rt+",  "+self.rs


iSet = {'R': ["add", "sub", "and", "or"],
        'I': ["addi", "lw", "sw"]
        }
depenOn=[]

class Itype:
    id = None
    type = None
    rs = None
    rt = None
    imm = None

    def __init__(self, id, type, rt, rs, imm):
        self.id = id
        self.type = type
        self.rt = rt
        self.rs = rs
        self.imm = imm

    def __str__(self):
        if (self.type == 'lw'):
            return self.type + "  " + self.rt + ",  " + self.imm + "(" + self.rs + ")"
        elif (self.type == 'sw'):
            return self.type + "  " + self.rs + ",  " + self.imm + "(" + self.rt + ")"
        else:
            return self.type + "  " + self.rt + ",  " + self.rs + ",  " + self.imm


def main():
    instQueue = []
    with open("instructions") as f:
        content = f.readlines()

    for i in content:
        if (i == "\n"):
            continue
        list = i.strip().split()
        if (iSet['R'].__contains__(list[1])):
            obj = Rtype(list[0], list[1], list[3].strip(","), list[4], list[2].strip(','))
        elif (iSet['I'].__contains__(list[1])):
            if (len(list) == 4):
                immediate = list[3][:-5]
                secondReg = list[3][-4:-1]
                if (list[1] == 'sw'):
                    obj = Itype(list[0], list[1], secondReg, list[2].strip(','), immediate)
                else:
                    obj = Itype(list[0], list[1], list[2].strip(','), secondReg, immediate)
            elif (len(list) == 5):
                obj = Itype(list[0], list[1], list[2].strip(','), list[3].strip(','), list[4])
        else:
            obj = "end"
        instQueue.append(obj)
    instQueue2=instQueue.copy()



    print("No Forwarding")
    print("All dependency :")
    checkNop(instQueue, 1, False)
    checkNop(instQueue, 2, False)
    print("All instructions")
    cnt=1
    for i in instQueue:
        print(cnt,"--> ",i)
        cnt+=1

    print("With Forwarding")
    print("All dependency :")
    checkNop(instQueue2, 1, True)
    print("All instructions")
    cnt=1
    for i in instQueue2:
        print(cnt, "--> ", i)
        cnt += 1

def checkNop(instQueue, cnt,forward):
    i = 0
    while instQueue[i + cnt] != 'end':

        inst1 = instQueue[i]
        inst2 = instQueue[i + cnt]
        if (inst1 == 'Nop'):
            i += 1
            continue
        if (inst2 == 'Nop'):
            i += 1
            continue
        nopCondtion = False
        if(forward):
            if(inst1.type=='lw'and inst1.rt in [inst2.rs,inst2.rt]):
                print(inst1.id,"-",inst2.id," on ",inst1.rt)
                instQueue.insert(i+1,'Nop')
        else:
            if set([inst1.type, inst2.type]).issubset(iSet['R']):
                if (inst1.rd in [inst2.rs, inst2.rt]):
                    print(inst1.id, "-", inst2.id, " on ", inst1.rd)
                    nopCondtion = True

            elif set([inst1.type, inst2.type]).issubset(iSet['I']):
                if (inst1.type == 'sw' and inst2.type == 'lw'):
                    i += 1
                    continue
                if (inst1.rt == inst2.rs):
                    print(inst1.id, "-", inst2.id, " on ", inst1.rt)
                    nopCondtion = True
            elif iSet['R'].__contains__(inst1.type) and iSet['I'].__contains__(inst2.type):

                if inst1.rd == inst2.rs:
                    print(inst1.id, "-", inst2.id, " on ", inst1.rd)
                    nopCondtion = True
            elif iSet['I'].__contains__(inst1.type) and iSet['R'].__contains__(inst2.type):
                if inst1.rt in [inst2.rs, inst2.rt]:
                    print(inst1.id, "-", inst2.id, " on ", inst1.rt)
                    nopCondtion = True

            if (nopCondtion):
                if (cnt == 1):
                    instQueue.insert(i + 1, 'Nop')
                    instQueue.insert(i + 2, 'Nop')
                if (cnt == 2):
                    instQueue.insert(i + 1, 'Nop')
        i += 1


if __name__ == '__main__':
    main()
