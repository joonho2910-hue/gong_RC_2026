import sys

def main():
    print(sys.argv, len(sys.argv))
    print("-----")
    print(sys.getprofile())
    print(sys.gettrace())
    print(sys.copyright)
    print(sys.version)
    print(sys.version_info)
    print(sys.flags)
    
    
    
if __name__ == "__main__":
    main()