#!/usr/bin/env python

data = """
commit 9721e0aae5aa695f002531ebfa208d6503d416b0
Author: Noor Mohamed <writetovaseem@gmail.com>
Date:   Wed Feb 3 13:25:07 2021 -0800

    feat: Upgrade to CUE v0.2.2

commit b57190d7317769da520063c447a5c7d6b5c0cd5d
Author: Noor Mohamed <writetovaseem@gmail.com>
Date:   Wed Feb 3 10:54:09 2021 -0800

    feat: Upgrade to bazel v4.0.0, rules_go v0.25.1, bazel-gazelle v0.22.3

commit 540ca8c02f438f7ef3e53d64d4e4e859d578cc15
Author: Noor Mohamed <writetovaseem@gmail.com>
Date:   Thu May 21 15:04:05 2020 -0700

    feat: Upgrade to CUE v0.2.0

    CUE toolchain, examples, and gazelle upgraded to v0.2.0

commit b80570334752adbad8fbc6559bc833090dbe7c5e
Author: Noor Mohamed <writetovaseem@gmail.com>
Date:   Mon May 11 09:42:47 2020 -0700

    feat: CUE 0.1.2 support

    CUE 0.1.2 becomes the default toolchain.
"""


def logparse(data):
    '''
    description: parse commit log based on commitid, author, date and msg
    type: data: string
    rtype: dict
    '''
    glog = data.split('\n')
    if not glog:
        return None

    READ_COMMIT = True
    cid = ''
    res = {}
    headers = {}
    msg = ''
    for line in glog:
        if not line:
            continue
        if line.startswith('commit ') and READ_COMMIT:
            cid = line[7:]                 # get commit id and set read_commit as false
            READ_COMMIT = False
            msg = ''
            headers = {}
        elif line.startswith('Author:'):   # instead of this 4 line, we can use regx
            headers['Author'] = line[7:]   # to match starting with author and date
        elif line.startswith('Date:'):     # add them to hashmap
            headers['Date'] = line[5:]
        else:
            if msg:
                msg = msg + '\n'
            msg = msg + ''.join(line.strip()) # append description to msg
            if not cid:
                raise "Commit sha not found"
            if not headers['Author']:
                raise "Author not found"
            if not headers['Date']:
                raise "Commit date not found"
            res[cid] = { 'headers' : headers , 'msg' : msg }
            READ_COMMIT = True                # reset read commit flag
    return res

import json
d = logparse(data)
print json.dumps(d, indent = 4)

#unit test
#successful testcase
#testcase1 empty string
assert logparse("") == {} , "Testcase - Failed - empty string"

#expected output
testcase2 = '''
commit 9721e0aae5aa695f002531ebfa208d6503d416b0
Author: Noor Mohamed <writetovaseem@gmail.com>
Date:   Wed Feb 3 13:25:07 2021 -0800

    feat: Upgrade to CUE v0.2.2
'''
expectedout={ "9721e0aae5aa695f002531ebfa208d6503d416b0": {
                "msg": "feat: Upgrade to CUE v0.2.2",
                "headers": {
                    "Date": "   Wed Feb 3 13:25:07 2021 -0800",
                    "Author": " Noor Mohamed <writetovaseem@gmail.com>"
                }
                }
         }
assert logparse(testcase2) == expectedout , "Testcase2 - Failed - output mismatched"

#failure usecase
'''
assert logparse("test") == {} , "Testcase3 - Failed - empty string"

expectedout={ "": {
                "msg": "feat: Upgrade to CUE v0.2.2",
                "headers": {
                    "Date": "   Wed Feb 3 13:25:07 2021 -0800",
                    "Author": " Noor Mohamed <writetovaseem@gmail.com>"
                }
                }
             }
assert logparse(testcase2) == expectedout , "Testcase4 - Failed - output mismatched"
'''
