import json

def file_write_json(filename, data):
    f = open(filename, 'w')
    json.dump(data, f, ensure_ascii=False)
    f.close()

def file_read_json(filename):
    f = open(filename, 'r')
    return json.load(f)

if __name__ == "__main__":
    print(f"This is mymodule: {__name__}")