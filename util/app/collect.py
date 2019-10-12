import sys

typeList = ["latest"]
trendingSourceList = ["itunes"]
transcribeList = ["google_cloud", "sphinx"]


def areArgsValid(args):
    return args[1] in typeList and args[2] in trendingSourceList and args[3] in transcribeList

def scrubArgs():

    expectedArgCount = 4
    expectedArgsTemplate = ("(type):\t\t<latest>\n"
    "(source):\t\t<itunes>\n"
    "(transcribe_method):\t<google_cloud\sphinx>\n"
    )
    expectedArgsExample = "collect -trending -itunes -sphinx"

    args = sys.argv
    argsCount = len(args)
    if argsCount < 2:
        print("Error: No arguments given. Type \"collect.py help\" for template")
        return False
    elif args[0].lower() is "help":
        print("Expected arguments:\n" + expectedArgsExample + "Example Useage:\n" + expectedArgsExample)
        return False
    elif argsCount == expectedArgCount and areArgsValid(args):
        print("Attempt to parse args")
        return True
    else:
        print("Error: Requires the expected arguments\n" + expectedArgsTemplate)
        return False



def main():
    doContinue = scrubArgs()
    if doContinue:
        print("Attempt to parse args")

main()