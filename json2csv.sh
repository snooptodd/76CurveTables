#! /bin/bash
## compare the live and pts json files for differences and if different plot them (maybe put the data in the plot too)
# for Live we need to search both json paths 
#  i suppose to start we get a list of all files in the ptsdir jsonalt dir 
#  then search the livedir for the same json files and compare (cmp) them ( we might(probably) need to prioritize jsonalt dir )
#  create a graph if they are different.
#  convert the json data to somthing gnuplot can understand (jq -r '.curve[]| join(" ")')
#  save the plot to svg or something.


RootDir='json'
LIVEDIR='Live'
PTSDIR='Pts_30Aug'
CommonDIR='misc/curvetables'

# get list of json files in jsonalt dir 
PTSDIRList="$(find $RootDir/$PTSDIR/$CommonDIR/jsonalt/ -iname "$1.json")"
# loop through PTSDIRList
for i in $PTSDIRList; do
	#strip the path 
	PTSJsonFile="$(basename $i)"
	LIVEDIRList="$(find $RootDir/$LIVEDIR/$CommonDIR/ -iname "$PTSJsonFile")"
	PTS=$(cat "$i" |jq -r '.curve[]| join(" ")')
	cat "$i" |jq -r '.curve[]| join(" ")' > ~/PTS
	#LIVEDIRAltList=`find /$RootDir/$LIVEDIR/$CommonDIR/jsonalt -iname "$PTSJsonFile"`
	# echo $PTSJsonFile
	# echo $LIVEDIRList
	Diff=0
	Jsonalt=0
	# LIVEDIRList only has the files that match the file we are looking for. so if jsonalt is found in the string then we only plot the jsonalt file. 
	if [[ $LIVEDIRList = *jsonalt* ]]; then
		Jsonalt=1
	fi
	for j in $LIVEDIRList; do
		#cmp files 
		if [[ $(cmp -s $i $j ) == 1 ]]; then
			Diff=1
		fi

		if [[ $j = *jsonalt* && $Jsonalt = 1 && $Diff = 1 ]]; then
			#echo $Jsonalt+$Diff $j
			Live=$(cat "$j" |jq -r '.curve[]| join(" ")')
			cat "$j" |jq -r '.curve[]| join(" ")' > ~/Live
		fi

		if [[ $Jsonalt = 0 && $Diff = 1 ]]; then
			#echo $Jsonalt+$Diff $j
			Live=$(cat "$j" |jq -r '.curve[]| join(" ")')
			cat "$j" |jq -r '.curve[]| join(" ")' > ~/Live
		fi

		if [[ $Diff = 1 ]]; then
			# gnuplot -p -e  'plot "$Live","$PTS" with lines'
			echo "Plotting $PTSJsonFile"

			echo "set title \"$(echo $PTSJsonFile|sed 's/_/ /g; s/\.json//')\" font \",15\" " > ~/SCRIP
			echo "set terminal png size 1024,1024" >> ~/SCRIP
			echo "set output \"$(echo ${PTSJsonFile//json/png/})\"" >> ~/SCRIP
			# echo "" >> ~/SCRIP
			# echo "" >> ~/SCRIP
			echo "plot \"~/Live\" with lines,\"~/PTS\" with lines" >> ~/SCRIP
			
			gnuplot -p ~/SCRIP
			# echo $Live
			# echo $PTS
		fi
		#echo $Jsonalt+$Diff $j
		Diff=0
		Jsonalt=0
	done

done
rm ~/Live ~/PTS ~/SCRIP
# OldName=$1$2
# NewName=`echo $1$2 |sed 's/\.json/\.csv/'`
# PTSFile=$1
# LiveList='find '
# echo $OldName
# echo $NewName
#cat "$OldName" |jq -r '.curve[]| join(",")' > "$NewName"
#gnuplot -e  'set terminal svg size 400,300; set output "health_alien.svg"; set datafile separator comma; plot "./health_alien.csv" with lines'
# gnuplot -p -e  'plot "$Live","$PTS" with lines'