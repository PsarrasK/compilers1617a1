
import sys
import re
import argparse


parser = argparse.ArgumentParser()
# add mandatory (positional) arguments
parser.add_argument("fname",help="input srt file name")
parser.add_argument("offset",type=float,help="subtitle offset in seconds to apply (can be fractional)")

# parse arguments
args = parser.parse_args()

#----------------------------1ST PART----------------------------#
restr = r'([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(,?)([0-9]*) --> ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(,?)([0-9]*)'
rexp = re.compile(restr)

#----------------------------2ND PART----------------------------#
value_given = float(sys.argv[2])
#print (value_given)

if value_given > 60:
	flseconds_to_add = float (value_given%60)
	seconds_to_add = int(value_given%60)
	subseconds_to_add = round(flseconds_to_add%1,3)
	subseconds_to_add = int (subseconds_to_add*1000)
	temp_minutes_to_add = int(value_given/60)
	hours_to_add = int(temp_minutes_to_add/60)
	minutes_to_add = temp_minutes_to_add%60
else:
	flseconds_to_add = float (value_given)
	seconds_to_add = int(value_given)
	subseconds_to_add = round(flseconds_to_add%1,3)
	subseconds_to_add = int (subseconds_to_add*1000)
	temp_minutes_to_add = 0
	hours_to_add = 0
	minutes_to_add = 0

	#print ("seconds_to_add: ", seconds_to_add)
	#print ("subseconds_to_add: ", subseconds_to_add)
	#print ("minutes_to_add: ", minutes_to_add)
	#print ("hours_to_add: ", hours_to_add)

#----------------------------3RD PART----------------------------#
with open(args.fname,newline='') as ifp:	
	for line in ifp:
		#----------------------------4TH PART----------------------------#
		l = rexp.finditer(line)
		k = rexp.search(line)
		#----------------------------5TH PART----------------------------#
		if k is None:
			sys.stdout.write(line)
		#----------------------------6TH PART----------------------------#
		for m in l:			
			if m is not None:
				new_subseconds1 = int(m.group(5))+subseconds_to_add
				new_seconds1 = int(m.group(3))+seconds_to_add
				new_minutes1 = int(m.group(2))+minutes_to_add
				new_hours1 = int(m.group(1))+hours_to_add

				if new_subseconds1 > 1000:
					new_seconds1 +=1
					new_subseconds1 -= 1000

				if new_seconds1 > 60:
					new_minutes1 +=1
					new_seconds1 -= 60

				if new_minutes1 > 60:
					new_hours1 +=1
					new_minutes1 -= 60

				new_subseconds2 = int(m.group(10))+subseconds_to_add
				new_seconds2 = int(m.group(8))+seconds_to_add
				new_minutes2 = int(m.group(7))+minutes_to_add
				new_hours2 = int(m.group(6))+hours_to_add

				if new_subseconds2 > 1000:
					new_seconds2 +=1
					new_subseconds2 -= 1000

				if new_seconds2 > 60:
					new_minutes2 +=1
					new_seconds2 -= 60

				if new_minutes2 > 60:
					new_hours2 +=1
					new_minutes2 -= 60
				
				#----------------------------7TH PART----------------------------#
				a = str(new_hours1).zfill(2)
				b = str(new_minutes1).zfill(2)
				c = str(new_seconds1).zfill(2)
				d = str(new_subseconds1).zfill(3)
				e = str(new_hours2).zfill(2)
				f = str(new_minutes2).zfill(2)
				g = str(new_seconds2).zfill(2)
				h = str(new_subseconds2).zfill(3)

				sys.stdout.write("{0}:".format(a))
				sys.stdout.write("{0}:".format(b))
				sys.stdout.write("{0},".format(c))
				sys.stdout.write("{0}".format(d))
				sys.stdout.write(" --> ")
				sys.stdout.write("{0}:".format(e))
				sys.stdout.write("{0}:".format(f))
				sys.stdout.write("{0},".format(g))
				sys.stdout.write("{0}".format(h))
				print("")
