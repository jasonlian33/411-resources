#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5001/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
    case $1 in
        --echo-json) ECHO_JSON=true ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
    echo "Checking health status..."
    curl -s -X GET "$BASE_URL/health" | grep -q '"status": "success"'
    if [ $? -eq 0 ]; then
        echo "Service is healthy."
    else
        echo "Health check failed."
        exit 1
    fi
}

# Function to check the database connection
check_db() {
    echo "Checking database connection..."
    curl -s -X GET "$BASE_URL/db-check" | grep -q '"status": "success"'
    if [ $? -eq 0 ]; then
        echo "Database connection is healthy."
    else
        echo "Database check failed."
        exit 1
    fi
}
############################################################
#
# Boxer Management
#
############################################################

create_boxer(){
    name=$1
    weight=$2
    height=$3
    reach=$4
    age=$5

    echo "Adding boxer ($name, $age) to the ring..."
    curl -s -X POST "$BASE_URL/create-boxer" -H "Content-Type: application/json" \
    -d "{\"name\":\"$name\", \"weight\":$weight, \"height\":$height, \"reach\":$reach, \"age\":$age}" | grep -q '"status": "success"'

    if [ $? -eq 0 ]; then
    echo "Boxer added successfully."
    else
        echo "Failed to add boxer."
        exit 1
    fi
}

delete_boxer_by_id(){
    boxer_id=$1

    echo "Deleting boxer by ID ($boxer_id)..."
    response=$(curl -s -X DELETE "$BASE_URL/delete-boxer-by-id/$boxer_id")
    if echo "$response" | grep -q '"status": "success"'; then
    echo "Boxer deleted successfully by ID ($boxer_id)."
    else
        echo "Failed to delete boxer by ID ($boxer_id)."
        exit 1
    fi
}

get_boxer_by_id(){
    boxer_id=$1

    echo "Getting boxer by ID ($boxer_id)..."
    response=$(curl -s -X GET "$BASE_URL/get-boxer-by-id/$boxer_id")
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Boxer retrieved successfully by ID ($boxer_id)."
        if [ "$ECHO_JSON" = true ]; then
        echo "Boxer JSON (ID $boxer_id):"
        echo "$response" | jq .
        fi
    else
        echo "Failed to get boxer by ID ($boxer_id)."
        exit 1
    fi
}

get_boxer_by_name(){
    boxer_name=$1

    echo "Getting boxer by name ($boxer_name)..."
    response=$(curl -s -X GET "$BASE_URL/get-boxer-by-name/$boxer_name")
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Boxer retrieved successfully by name ($boxer_name)."
        if [ "$ECHO_JSON" = true ]; then
        echo "Boxer JSON (name $boxer_name):"
        echo "$response" | jq .
        fi
    else
        echo "Failed to get boxer by name ($boxer_name)."
        exit 1
    fi

}

############################################################
#
# Ring Management
#
############################################################

# not sure how to implemenet/need to implement
fight(){
    echo "Initiating fight ..."
    response=$(curl -s -X POST "$BASE_URL/begin-fight")

    if echo "$response" | grep -q '"status": "success"'; then
        echo "Fight starts and ends with one winner."
    else
        echo "Failed to start fight."
        exit 1
    fi

}

clear_ring(){
    echo "Clearing ring..."
    response=$(curl -s -X POST "$BASE_URL/clear-ring")

    if echo "$response" | grep -q '"status": "success"'; then
        echo "Ring cleared successfully."
    else
        echo "Failed to clear ring."
        exit 1
    fi
}

enter_ring(){
    boxer_id=$1
    boxer_name=$2
    boxer_age=$3
    
    echo "Entering boxer to the ring: $boxerid: $boxer_name ($boxer_age) ..."
    response=$(curl -s -X POST "$BASE_URL/enter-boxer-to-ring" \
        -H "Content-Type: application/json" \
        -d "{\"boxer_id\":\"$boxer_id\", \"boxer_name\":\"$boxer_name\", \"boxer_age\":$year}")

    if echo "$response" | grep -q '"status": "success"'; then
        echo "Song added to playlist successfully."
        if [ "$ECHO_JSON" = true ]; then
        echo "Song JSON:"
        echo "$response" | jq .
        fi
    else
        echo "Failed to add song to playlist."
        exit 1
    fi
}

get_boxers(){
    echo "Retrieving all boxers from the ring..."
    response=$(curl -s -X GET "$BASE_URL/get-all-boxers-from-ring")

    if echo "$response" | grep -q '"status": "success"'; then
        echo "All boxers retrieved successfully."
        if [ "$ECHO_JSON" = true ]; then
        echo "Boxers JSON:"
        echo "$response" | jq .
        fi
    else
        echo "Failed to retrieve all boxers from ring."
        exit 1
    fi
    
}


######################################################
#
# Leaderboard
#
######################################################

# Function to get the boxing leaderboard sorted by play wins
get_boxing_leaderboard(){
    echo "Getting boxing leaderboard sorted by play wins..."
    response=$(curl -s -X GET "$BASE_URL/boxing-leaderboard?sort=wins")
    if echo "$response" | grep -q '"status": "success"'; then
        echo "Boxing leaderboard retrieved successfully."
        if [ "$ECHO_JSON" = true ]; then
        echo "Leaderboard JSON (sorted by wins):"
        echo "$response" | jq .
        fi
    else
        echo "Failed to get boxing leaderboard."
        exit 1
    fi
}

# Initialize the database
sqlite3 db/boxing.db < sql/init_db.sql

# Health checks
check_health
check_db

# Create Boxers
create_boxer "Alex" 180 185 80 24
create_boxer "Jordan" 168 175 73 35
create_boxer "Ben" 200 191 82 30
create_boxer "Phil" 172 145 70 22
create_boxer "Dan" 178 172 68 27
create_boxer "Bot" 175 178 76 39

delete_boxer_by_id 1
get_boxers

get_boxer_by_id 2
get_boxer_by_name "Bot"
get_boxer_by_name "Dan"

enter_ring 3 "Ben" 30
enter_ring 4 "Phil" 22
fight #might need to move somewhere else

clear_ring

get_boxing_leaderboard

echo "All tests passed successfully!"



