#! /bin/bash
## compare the live and pts json files for Differences and if Different plot them (maybe put the data in the plot too)
# for Live we need to search both json paths 
#  i suppose to start we get a list of all files in the ptsdir jsonalt dir 
#  then search the livedir for the same json files and compare (cmp) them ( we might(probably) need to prioritize jsonalt dir )
#  create a graph if they are Different.
#  convert the json data to somthing gnuplot can understand (jq -r '.curve[]| join(" ")')
#  save the plot to svg or something.


RootDir="json"
livePatch='Live_P54'
LIVEDIR="$livePatch"
PTSDIR='PTS_27Sep24'
CommonDIR='misc/curvetables'
SearchName="${1:=*}"
#SearchName="health_alien"

MakeGraph() {
	echo "Plotting $PTSJsonFile"
	Live=$(jq -r '.curve[]| join(" ")' "$jLive")
	printf %s "$Live" > ./$livePatch

	#its ugly, but works. 
	echo "set title \"$(echo "$PTSJsonFile"|sed 's/_/ /g; s/\.json//')\" font \",15\" " > ./SCRIP
	echo 'set terminal png size 1024,1024' >> ./SCRIP
	echo "set output \"./graphs/$PTSJsonPath/$(echo "${PTSJsonFile//json/png}")\"" >> ./SCRIP
	# echo "" >> ./SCRIP
	# echo "" >> ./SCRIP
	# echo "plot \"./Live\" with lines, " >> ./SCRIP
	# echo "\"./PTS\" with lines, " >> ./SCRIP
	# echo "\"./PTS\" every 10 with labels notitle" >> ./SCRIP
	# echo 'plot "./Live" with lines,"./PTS" with linespoint,"./PTS" using 1:2:(sprintf("%d", $2)) every 5 with labels notitle' >> ./SCRIP
	echo 'plot "'$livePatch'" with lines,"'$PTSDIR'" with linespoint' >> ./SCRIP

	mkdir -p "./graphs/$PTSJsonPath"
	gnuplot -p ./SCRIP
}

# get list of json files in jsonalt dir 
PTSDIRList=$(find ./$RootDir/$PTSDIR/$CommonDIR/jsonalt/ -iname "$SearchName.json")
# loop through PTSDIRList
for iPTS in $PTSDIRList; do
	#strip the path 
	PTSJsonFile=$(basename "$iPTS")
	# echo "dirname "$iPTS"|sed s/..$RootDir.$PTSDIR.$CommonDIR.jsonalt.//"
	PTSJsonPath=$(dirname "$iPTS"|sed s/..$RootDir.$PTSDIR.misc.curvetables.jsonalt.//)
	# get list of files in livedir that match iPTS
	LIVEDIRList=$(find ./$RootDir/$LIVEDIR/$CommonDIR/ -iname "$PTSJsonFile")

	# if $LIVEDIRList is has more than 2 entries we will have probalems lets check for it and hope it never happens. 
	if [[ ${#LIVEDIRList[@]} -gt 2 ]]; then
		echo "shit more than two files found that match"
		echo ${#LIVEDIRList[@]}
		# stop the script 
		return
	fi

	PTS=$(jq -r '.curve[]| join(" ")' "$iPTS")
	printf %s "$PTS" > ./$PTSDIR

	Diff=0
	Jsonalt=0
	# LIVEDIRList only has the files that match the file we are looking for. so if jsonalt is found in the string then we only plot the jsonalt file. 
	if [[ $LIVEDIRList = *jsonalt* ]]; then
		Jsonalt=1
	fi

	for jLive in $LIVEDIRList; do

		#cmp files 
		if [[ ! $(cmp -s "$iPTS" "$jLive") ]]; then
			Diff=1
		fi
		# We only want to create 1 graph from the files that match $iPTS and we want to prioritize the jsonalt folder
		# so we need to check if $jLive currently contains jsonalt
		# and if jsonalt was found at all in the list 
		# and no reason to make the graph if there is no change.
		if [[ $jLive == *jsonalt* && $Jsonalt -eq "1" && $Diff -eq "1" ]]; then
			MakeGraph
		elif [[ $Jsonalt -eq "0" && $Diff -eq "1" ]]; then
			MakeGraph
		fi
		

			# echo "$jLive"
			# echo "$iPTS"
			# echo "jsonalt = $Jsonalt"
			# echo "Diff = $Diff"
	done

done
rm ./$livePatch ./$PTSDIR ./SCRIP

# OldName=$1$2
# NewName=`echo $1$2 |sed 's/\.json/\.csv/'`
# PTSFile=$1
# LiveList='find '
# echo $OldName
# echo $NewName
#cat "$OldName" |jq -r '.curve[]| join(",")' > "$NewName"
#gnuplot -e  'set terminal svg size 400,300; set output "health_alien.svg"; set datafile separator comma; plot "./health_alien.csv" with lines'
# gnuplot -p -e  'plot "$Live","$PTS" with lines'