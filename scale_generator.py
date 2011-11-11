#(C)2011 Garrett Grimm
#www.grimmdude.com
#www.musictheory.com/scale-generator

def scaleGen(start = 0, scale = 'major'):
	
	#define notes
	notes = {
		'sharps' : ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'],
		'flats' : ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
	};
	
	#define scale types
	#these are intervals between notes, 1:half step, 2:whole step
	scales = {
		'major' : [2, 2, 1, 2, 2, 2],
		'blues' : [3, 2, 1, 1, 3],
		'natural_minor' : [2, 1, 2, 2, 1, 2],
		'harmonic_minor' : [2, 1, 2, 2, 1, 3],
		'melodic_minor' : [2, 1, 2, 2, 2, 2, 1, -2, -2, -1, -2, -2, -1, -2]
	}
	
	#define triad intervals
	triads = {
		'major' : [4, 3],
		'minor' : [3, 4],
		'dim' : [3, 3],
		'aug' : [4, 4]
	}

	#assign to scaleIntervals
	scaleIntervals = scales[scale];
	
	#specify which notes to use for this key.
	if (scaleIntervals != scales['major']):
		#specify which 'notes' array to use for minor keys
		if (start == 0 or start == 1 or start == 2 or start == 3 or start == 5 or start == 7 or start == 8 or start == 10):
			notes_array = notes['flats']
		else:
			notes_array = notes['sharps']
 	
	else:
		#specify which 'notes' array to use for major keys
		if (start == 1 or start == 3 or start == 5 or start == 8 or start == 10):
			notes_array = notes['flats']
		else:
			notes_array = notes['sharps']
	
	#object to contain all results from this function, starting with the_scale
	the_key = {
		'the_scale': [],
		#CREATE arrays of diatonic triads/names and sevenths
		'diatonic_triad_notes' : [],
		'diatonic_triad_names' : [],
		'diatonic_sevenths_notes' : [],
		'scale_type' : scale,
		'root' : notes_array[start],
		'scale_intervals' : scaleIntervals
	}
	
	#shortcut for accessing the_key.the_scale
	s = the_key['the_scale']	
	
	#create new array from scale to reference each note from the starting note.  Used in loop below.
	start_reference = []
	total = 0
	
	#CREATE the_scale
	#use the start_reference array to pull notes from the notes array 
	#referencing from the start note.
	i = 0

	while (i <= len(scaleIntervals)):
		
		#add the current interval and add one by one to the start_reference array
		if i < len(scaleIntervals):
			total += scaleIntervals[i]	
			
		start_reference.append(total)

		#minus 1 to account for the starting note
		if (i == 0):
			current_note = start
		else:
			current_note = start + start_reference[i - 1]

		#loop back around the notes array if current>notes.length
		if (current_note >= len(notes_array)):
			current_note = current_note - 12

		s.append(notes_array[current_note])
		i += 1
	
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