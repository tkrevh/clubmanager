from django import template

# Set register
register = template.Library()

# Register filter
@register.filter
def sectodur(value):
	
	"""
	#######################################################
	#                                                     #
	#   Seconds-to-Duration Template Tag                  #
	#   Dan Ward 2009 (http://d-w.me)                     #
	#                                                     #
	#######################################################
	"""
		
	# Place seconds in to integer
	secs = int(value)
	
	# If seconds are greater than 0
	if secs > 0:
		
		# Import math library
		import math
		
		# Place durations of given units in to variables
		daySecs = 86400
		hourSecs = 3600
		minSecs = 60
		
		# Create string to hold outout
		durationString = ''
		
		# Calculate number of hours from seconds (minus number of days)
		hours = int(math.floor(secs / int(hourSecs)))
		
		# Subtract hours from seconds
		secs = secs - (hours * int(hourSecs))
		
		# Calculate number of minutes from seconds (minus number of days and hours)
		minutes = int(math.floor(secs / int(minSecs)))
		
		# Subtract days from seconds
		secs = secs - (minutes * int(minSecs))
		
		# Calculate number of seconds (minus days, hours and minutes)
		seconds = secs
		
		durationString += str(hours).rjust(2, '0') + ':' + str(minutes).rjust(2, '0') + ':' + str(seconds).rjust(2, '0')
			
		# Return duration string
		return durationString.strip()
		
	else:
		
		#  'No duration'
		return '00:00:00'