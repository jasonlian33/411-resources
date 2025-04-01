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
    curl -s -X POST "$BASE_URL/add-boxer" -H "Content-Type: application/json" \
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
    response=$(curl -s -X DELETE "$BASE_URL/delete-boxer/$boxer_id")
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

fight(){
    echo "Initiating fight ..."
    response=$(curl -s -X GET "$BASE_URL/fight")

    if echo "$response" | grep -q '"status": "success"'; then
        echo "Fight starts and ends with one winner."
    else
        echo "Failed to start fight."
        exit 1
    fi

}

clear_boxers(){
    echo "Clearing boxers from ring..."
    response=$(curl -s -X POST "$BASE_URL/clear-boxers")

    if echo "$response" | grep -q '"status": "success"'; then
        echo "Ring cleared successfully."
    else
        echo "Failed to clear ring."
        exit 1
    fi
}


enter_ring(){
    boxer_name=$1
    boxer_age=$2

    echo "Entering boxer to the ring: $boxer_name ($boxer_age) ..."
    response=$(curl -s -X POST "$BASE_URL/enter-ring" \
        -H "Content-Type: application/json" \
        -d "{\"name\": \"$boxer_name\", \"boxer_age\": $boxer_age}")

    if echo "$response" | grep -q '"status": "success"'; then
        echo "Boxer added to ring successfully."
        if [ "$ECHO_JSON" = true ]; then
            echo "Boxer JSON:"
            echo "$response" | jq .
        fi
    else
        echo "Failed to add boxer to ring."
        exit 1
    fi
}


get_boxers(){
    echo "Retrieving all boxers from the ring..."
    response=$(curl -s -X GET "$BASE_URL/get-boxers")

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
    response=$(curl -s -X GET "$BASE_URL/leaderboard?sort=wins")
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

#Create Boxers
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

clear_boxers

enter_ring "Ben" 30
enter_ring "Phil" 22
fight 

clear_boxers

get_boxing_leaderboard

echo "All tests passed successfully!"





