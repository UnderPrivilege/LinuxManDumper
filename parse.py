import re
import signal
import sys

json_content = "{\n"


def handler(signum, frame):
	save_json()

def main(man_path):
	global json_content
	skips = 0
	signal.signal(signal.SIGINT, handler)
	man_file = open(man_path, "r")
	man_buffer = man_file.read()
	print("[+] Manual Loaded")

	i = 0

	man_stream = ""
	total_len = len(man_buffer)
	while i < total_len:
		arrows = int(i/total_len*30)
		print("Dumping functions "+str(i)+"/"+str(total_len)+" ["+(arrows*"=")+">"+((29-arrows)*" ")+"] "+str(skips)+" skips\t\r",end="")
		sys.stdout.flush()

		try:
			man_stream += man_buffer[i]

			'''
				We start by finding the Manual Number for Info
			'''
			pattern = "\.TH ([A-Za-z0-9]+) ([0-9]+)"
			man_pattern = re.search(pattern, man_stream)
			while not man_pattern:
				i += 1
				man_stream += man_buffer[i]
				man_pattern = re.search(pattern, man_stream)

			man_number = man_pattern.group(2)
			'''
				We now treat the  different function names
			'''
			pattern = "\.SH NAME"
			while not re.search(pattern, man_stream):
				man_stream += man_buffer[i]
				i += 1

			man_stream = ""
			pattern = "\.SH SYNOPSIS"
			failed_flag = False
			while not re.search(pattern, man_stream):
				man_stream += man_buffer[i]
				if "Perl" in man_stream:
					failed_flag = True

				i += 1
			if failed_flag:
				continue

			names = man_stream.split("\-")
			if(len(names) == 1):
				names = man_stream.split("-")
			names[-1] = names[-1][:names[-1].find("\n")].rstrip().lstrip()

			functions_names = names[0].split(",")
			description 	= names[1]

			fatal_flag = False
			for j in range(len(functions_names)):
				fname = functions_names[j]
				if "Linux Programmer's Manual" in fname or "Redland RDF Application Framework" in fname or "GNU gettext" in fname:
					fatal_flag = True

				functions_names[j] = functions_names[j].lstrip().rstrip().replace("\n","")

			if(fatal_flag):
				skips += 1
				continue

			#print(man_stream)
			'''
				We now treat the include headers and all of the function signatures
			'''
			man_stream = ""
			pattern = "\.SH DESCRIPTION"
			while not re.search(pattern, man_stream):
				man_stream += man_buffer[i]
				i+=1

			pattern = "\#include <([A-Za-z0-9]+(.h))>"
			headers = [x.group(1) for x in re.finditer( pattern, man_stream)]

			pattern = "((int|long|unsigned|signed|void|float|double|struct|char|const|FILE|typedef|[A-Za-z]+_t)\** (.|\n)+?(?=;))"
			functions = [x.group() for x in re.finditer( pattern, man_stream)]

			#Clean some things inside the function
			for j in range(len(functions)):
				functions[j] = re.sub("(\"|;|\\n|\.[A-Z]{2})","", functions[j])

			if len(functions_names) != len(functions):
				skips += 1
				continue
			
			'''
				Now we can treat the description of the functions
			'''
			man_stream = ""
			pattern = "(\.SH RETURN VALUE|\.SH ATTRIBUTES)"
			while not re.search(pattern, man_stream):
				man_stream += man_buffer[i]
				i+=1

			pattern = "(\.[A-Za-z]{,2})"
			man_stream = re.sub(pattern, " ", man_stream)
			man_stream = re.sub("\ {2,}", " ", man_stream)
			man_stream = re.sub("^\n+", "", man_stream)

			man_stream = man_stream.replace("\\","").replace("\t"," ")
			pattern = "(RETURN VALUE|ATTRIBUTES)"
			man_stream = re.sub(pattern, "",man_stream)

			LIMIT = 600
			if(len(man_stream) > LIMIT):
				man_stream = man_stream[:LIMIT] + "..."
			full_description = man_stream

			'''
				We can now write what we found in the JSON file
			'''
			for j in range(len(functions_names)):
				name = functions_names[j]
				prototype     = re.sub(" {2,}", " ", functions[j])
				prototype     = re.sub("\\", " ", functions[j])
				header        = ", ".join(headers)

				json_content += "\t\"%s\": {\n\t\t\"descr\": \"%s\",\n\t\t\"name\": \"%s\",\n\t\t\"params\":[],\n\t\t\"path\": \"%s\",\n\t\t\"syntax\": \"%s\",\n\t\t\"type\": \"Linux API (man %s)\"\n\t},\n" % (name, description, name, header , prototype, man_number)
			i += 1
		except IndexError:
			print("\n[+] Finished Dumping, writing to JSON")
			break
	save_json()

def save_json():
	global json_content
	json_content += "\n}"

	f = open("C.json", "w")
	f.write(json_content)
	f.close()
	print("[+] Everything was successfully saved")
	
if __name__ == '__main__':
	if(len(sys.argv) < 2):
		print("Usage: parse man_page.txt")
		exit()
	main(sys.argv[1])