#!/usr/bin/python
# 2011 Garrett Grimm
# www.grimmdude.com

# Import sys module for command line operations
import sys

def customScale(notes):
	
	return
	
def pentatonic(root = 'C', scale = 'major'):
	"""
	Returns the pentatonic scale of the given root and scale type (major or minor)
	"""
	
	actual_scale = scale
	
	# If minor just pass 'natural_minor' to the makeScale function since 'minor' isn't an available arg.
	if scale == 'minor':
		actual_scale = 'natural_minor'
	
	# Get the full scale
	s = makeScale(root, actual_scale)
	
	if scale == 'major':
		pentatonic = [s[0], s[1], s[2], s[4], s[5]]
		
	elif scale == 'minor':
		pentatonic = [s[0], s[2], s[3], s[4], s[6]]
		
	else:
		return None
	
	return pentatonic
	
def guessChord(notes):
	"""
	Takes a list of notes and returns the most likely chord name as a string.
	"""
	
	# If there are only 3 notes it might be a triad.  Quick and easy test:
	if len(notes) == 3 and triadType(notes):
		
		# Return chord type string
		return notes[0] + ' ' + triadType(notes) + ' ' + 'triad'
		
	# Maybe it's a 
	
	# Convert notes to numbers
	notes = [noteToNumber(n)  for n in notes ]
	
	# Put numbers in ascending order
	notes = sorted(notes)
	
	
	
	return notes

def noteToNumber(note_):
	"""
	Convert a note name into it's corresponding number or vice versa.  
	"""
	
	# Define natural notes
	notes_numbers = {'C' : 0, 'D' : 2, 'E' : 4, 'F' : 5, 'G' : 7, 'A' : 9, 'B' : 11}
	
	# Create a reversed version of notes_numbers dict (number:note)
	numbers_notes = {}
	for n in notes_numbers:
		numbers_notes[notes_numbers[n]] = n
	
	# Define accidental values
	accidentals = {'#' : 1, 'b' : -1}
	
	
	# Check to see if this is a number
	if note_ in str(range(12)):
		
		# Convert it to an int
		note_ = int(note_)
		
		# First check if it's a natural note
		if note_ in numbers_notes.keys():
			return_note = numbers_notes[note_]
			
			return return_note
			
		# If it's not a natural note then we need to add accidentals to get the number to match
		else:
			return_note = numbers_notes[note_ + accidentals['#']]  + accidentals.keys().index('#')
		
		
			
	# It's a note name, not a number
	else:
		# No accidental
		if len(note_) == 1:
			return_number = notes_numbers[note_]
		
		# Single accidental
		if len(note_) == 2:
			return_number = notes_numbers[note_[0]] + accidentals[note_[1]]
		
		# Fix negative numbers
		if return_number < 0:
			return_number = return_number + 12
		
		return return_number
		
		
def relativeKey(root = 'C', scale = 'major'):
	"""
	Returns the root note of the relative key.
	
	scale = 'major' or 'minor'
	"""
	
	actual_scale = scale
	
	# If minor just pass 'natural_minor' to the makeScale function since 'minor' isn't an available arg.
	if scale == 'minor':
		actual_scale = 'natural_minor'
	
	# First make the requested scale
	s = makeScale(root, actual_scale)
	
	if scale == 'major':
		relative = s[5]
		
	elif scale == 'minor':
		relative = s[2]
		
	else:
		relative = None
	
	return relative

def noteInterval(note1, note2, numbers = False):
	"""
	Returns the number interval of two given notes
	"""
	
	if not numbers:
		# Convert notes to numbers
		note1 = noteToNumber(note1)
		note2 = noteToNumber(note2)
	
	interval = note2 - note1
	
	# If we've gone around master note list interval will be negative.  Resolve by adding 12.
	if interval < 0:
		interval = interval + 12
		
	return interval
	

def triadNotes(root = 'C', scale = 'major', return_numbers = False):
	"""
	Returns a list of notes for a given triad.  Can be returned in notes or number format.
	"""
	
	# Need to support aug,dim.  Currently just supports major & minor.
	
	actual_scale = scale
	
	if scale == 'minor':
		actual_scale = 'natural_minor'

	# Get the scale
	scale = makeScale(root, actual_scale)

	triad = [scale[0], scale[2], scale[4]]

	if return_numbers:
		# Make the numbers triad from the notes triad
		triad = [noteToNumber(n) for n in triad]

	return triad

	
def triadType(notes):
	"""
	Takes a list of 3 note names and returns triad name string.  Returns None if there's no match.
	"""
	
	# Define triad intervals
	triads = {
		'major' : [4, 3],
		'minor' : [3, 4],
		'dim' : [3, 3],
		'aug' : [4, 4]
	}
	
	# Convert notes to a list of numbers
	notes = [noteToNumber(n) for n in notes]
	
	# Sort notes so that they are in order
	## Code here...

	notes_intervals = []
	
	# Loop through notes and create a list, length 2, of intervals to check against
	for i in range(2):
		
		interval = noteInterval(notes[i], notes[i+1], True)
			
		notes_intervals.append(interval)
	
	# Finally loop through the traids dict to see if we have a match	
	for t in triads.keys():
		if triads[t] == notes_intervals:
			return t
		
	return None
	
def makeScale(root = 'C', scale = 'major', return_numbers = False):
	"""
	Generates a list of notes or corresponding numbers forming the specified scale.
	
	return_type = 'notes'/'numbers'
	scale = 'major'/'natural_minor'/ 
	"""
	
	# Convert root to a number 1-12
	root = noteToNumber(root)
	
	# Define notes in sharps/flats groups
	notes = {
		'sharps' : ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
		'flats' : ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
	};
	
	# Define the possible scale intervals
	scales = {
		'major' : [2, 2, 1, 2, 2, 2],
		'blues' : [3, 2, 1, 1, 3],
		'natural_minor' : [2, 1, 2, 2, 1, 2],
		'harmonic_minor' : [2, 1, 2, 2, 1, 3],
		'melodic_minor' : [2, 1, 2, 2, 2, 2, 1, -2, -2, -1, -2, -2, -1, -2]
	}
	
	#specify which notes to use for this key.
	if (scales[scale] == scales['major']):
		#specify which 'notes' array to use for major keys
		if root in [1, 3, 5, 8, 10]:
			notes_array = notes['flats']
		else:
			notes_array = notes['sharps']
	
	else:
		#specify which 'notes' array to use for minor keys
		if root in [0, 1, 2, 3, 5, 7, 8, 10]:
			notes_array = notes['flats']
		else:
			notes_array = notes['sharps']
	
	# List to contain all results from this function, starting with the_scale
	return_scale = []	
	
	# Create new array from scale to reference each note from the starting note.  Used in loop below.
	start_reference = []
	total = 0
	
	# Create return_scale list
	# Use the start_reference array to pull notes from the notes array 
	# Referencing from the root note.
		
	for i in range(len(scales[scale])+1):
		
		#add the current interval and add one by one to the start_reference array
		if i < len(scales[scale]):
			total += scales[scale][i]	
			
		start_reference.append(total)

		#minus 1 to account for the starting note
		if i == 0:
			current_note = root
		else:
			current_note = root + start_reference[i - 1]

		#loop back around the notes array if current>notes.length
		if current_note >= len(notes_array):
			current_note = current_note - 12
			
		# Generate notes or numbers, depending on the argument passed
		if not return_numbers:
			return_scale.append(notes_array[current_note])
			
		elif return_numbers:
			return_scale.append(noteToNumber(notes_array[current_note]))
			
		else:
			return None
			
		
	return return_scale


def scaleGen(start = 0, scale = 'major'):
	
	"""
	Scale Gen Helps
	
	"""
	
	#POST SCALE CREATION OBJECT KEYS
	#GET relative_major/minor
	if (scaleIntervals != scales['major']):
		the_key['relative_major'] = s[2]
		the_key['relative_major_ref'] = notes_array.index(s[2])

	else:
		the_key['relative_minor'] = s[5]
		the_key['relative_minor_ref'] = notes_array.index(s[5])
	
	#CREATE pentatnoic_scale
	if (scaleIntervals != scales['major']):
		the_key['pentatonic_scale'] = [s[0], s[2], s[3], s[4], s[6]]
		 
	else:
		the_key['pentatonic_scale'] = [s[0], s[1], s[2], s[4], s[5]]
	
	#use this function to create diatonic chords from the current note by stacking thirds
	#in the 'for' loop below.
	#ie: chord_note(1) gets root, chord_note(3) gets third etc.
	def chord_note(degree):
		
		#minus one because i starts on 0.
		degree = degree - 1
		
		if (i + degree >= len(s)):
			return (i + degree) - len(s)
			
		else:
			return i + degree
	
	#The slightly messy 'for' loop which creates all diatonic chords and chord names.
	i = 0
	while (i < len(s)):

		#create the diatonic_triad_notes array for this note
		the_key['diatonic_triad_notes'].append([s[chord_note(1)], s[chord_note(3)], s[chord_note(5)]])
		
		#create the diatonic_sevenths_notes array for this note
		the_key['diatonic_sevenths_notes'].append([s[chord_note(1)], s[chord_note(3)], s[chord_note(5)], s[chord_note(7)]])
		
		#if the third < first, or fifth < third add the length of the scale to get the extended number
		#so we can add/subract to get major/minor/dim/aug intervals.
		if (notes_array.index(s[chord_note(3)]) < notes_array.index(s[chord_note(1)])):
			third_extend = notes_array.index(s[chord_note(3)]) + len(notes_array)
		else:
			third_extend = notes_array.index(s[chord_note(3)])
			
		if (notes_array.index(s[chord_note(5)]) < third_extend ):
			fifth_extend = notes_array.index(s[chord_note(5)]) + len(notes_array)
		else:
			fifth_extend = notes_array.index(s[chord_note(5)])
			
		#define the formulas for each triad type by using the notes_array index.  
		first_third = third_extend - notes_array.index(s[chord_note(1)])
		second_third = fifth_extend - third_extend
		
		if (first_third == triads['major'][0] and second_third == triads['major'][1]):
			the_key['diatonic_triad_names'].append(s[i] + 'M')
			
		elif (first_third == triads['minor'][0] and second_third == triads['minor'][1]):
			the_key['diatonic_triad_names'].append(s[i] + 'm')

		elif (first_third == triads['dim'][0] and second_third == triads['dim'][1]):
			the_key['diatonic_triad_names'].append(s[i] + 'dim')
			
		elif (first_third == triads['aug'][0] and second_third == triads['aug'][1]):
			the_key['diatonic_triad_names'].append(s[i] + 'aug')
		
		#define formulas for seventh chords - currently not being utilized
		#elif (first_third == triads['major'][0] and second_third == triads['major'][1]):


		#elif (first_third == triads['major'][0] and second_third == triads['major'][1]):

			
		#elif (first_third == triads['major'][0] and second_third == triads['major'][1]):
		
		i += 1

	return the_key
	
def main():
	# Command line goodies.
	
	# Check for args starting at index 1 since 0 is the script itself
  	args = sys.argv[1:]
	
	if not args:
		print 'usage: [--flag] arguments'
		sys.exit(1)
		
	# makeScale()
	if args[0] in ['--makeScale', '-ms']:
		if len(args) == 3:
			print makeScale(args[1], args[2])
			
		else:
			print 'usage: [--makeScale, -ms] note scale'
			
	# triadNotes()
	if args[0] in ['--triadNotes', '-tn']:
		if len(args) == 3:
			print triadNotes(args[1], args[2])
			
		else:
			print 'usage: [--triadNotes, -tn] root scale'
			
	# triadType()
	if args[0] in ['--triadType', '-tt']:
		if len(args) == 4:
			
			# Put the argument notes into an array
			arg_notes = []
			
			for n in args[1:]:
				arg_notes.append(n)
				
			print triadType(arg_notes)
		
		else:
			print 'usage: [--triadType, -tt] notes'

	# NoteToNumber()
	if args[0] in ['--noteToNumber', '-nn']:
		if len(args) == 2:
			print noteToNumber(args[1])
		
		else:
			print 'usage: [--noteToNumber, -nn] note'
			
	# pentatonic()
	if args[0] in ['--pentatonic', '-p']:
		if len(args) == 3:
			print pentatonic(args[1], args[2])
			
		else:
			print 'usage: [--pentatonic, -p] note scale'
			
	# guessChord()
	if args[0] in ['--guessChord', '-gc']:
			if len(args) > 1:
				# Put the argument notes into an array
				arg_notes = []
				
				for n in args[1:]:
					arg_notes.append(n)
					
				print guessChord(arg_notes)
				
			else:
				print 'usage: [--guessChord, -gc] note note ...'
				

	
if __name__ == '__main__':
	main()