import csv

projects_per_year = {}
owner_count_per_year = {}
owners_and_years = {}

min_year = 9999
max_year = -9999

with open('/Users/ahmedsiddiqui/Desktop/Workspace/UVic/Fall_2021/SENG480B/pypi-scraper/data/all_eggs_data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    is_data = 0
    for row in csv_reader:
        if is_data == 0:
            is_data += 1
        else:
            name = row[0]
            release_year = int(row[1])
            if release_year < min_year:
                min_year = release_year
            if release_year > max_year:
                max_year = release_year
            downloads = int(row[2])
            owners = row[3].split(',')
            owner_urls = row[4].split(',')
            projects_per_year[release_year] = projects_per_year.get(release_year, 0) + 1
            for owner in owners:
                if owners_and_years.get(owner):
                    if owners_and_years[owner][0] < release_year:
                        owners_and_years[owner].append(release_year)
                    else:
                        owners_and_years[owner].insert(0, release_year)
                else:
                    owners_and_years[owner] = [release_year]


for owner in owners_and_years:
    year = owners_and_years[owner][0]
    owner_count_per_year[year] = owner_count_per_year.get(year, 0) + 1

with open('/Users/ahmedsiddiqui/Desktop/Workspace/UVic/Fall_2021/SENG480B/pypi-scraper/data/users_and_projects_per_year.csv', mode='w') as csv_file:
    fieldnames = ['year', 'projects', 'users']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    number_of_projects = 0
    number_of_owners = 0
    for year in range(min_year, max_year + 1):
        number_of_projects += projects_per_year[year]
        number_of_owners += owner_count_per_year[year]
        writer.writerow({'year': year, 'projects': number_of_projects, 'users': number_of_owners})
        # print(f"Year {year} projects {number_of_projects} owners {number_of_owners}")
