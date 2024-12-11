def readPostsIdsFromCSVFile(input_path):
    print("Reading posts IDs from CSV file...")
    posts_ids = []
    with open(input_path, 'r') as file:
        for line in file:
            posts_ids.append(line.strip())
    return posts_ids