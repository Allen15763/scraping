import requests

request_url = "http://data.nba.net/prod/v2/2019/teams.json"
response = requests.get(request_url)
response_json = response.json()
teams = response_json["league"]["standard"]  #共分兩層

nba_teams_count = 0
for d in teams:
	if d['isNBAFranchise']:  #原值是布林不需==  (isNBAFrancjise = True)
		nba_teams_count += 1

print("2019-2020 球季 NBA 有 {} 支球隊".format(nba_teams_count))  #.format給條件



team_dict = {}
for t in teams:
    div = t["divName"]
    full_name = t["fullName"]
    if div in team_dict:   #For拿出每一筆，如果x在字典內，給對應值，沒有則擷取x和對應值
        team_dict[div].append(full_name)
    else:
        team_dict[div] = [full_name]

# print(team_dict)
# for a in team_dict:
# 	if a['divName'] == Atlantic or a['divName'] == Southwest

specific_teams_count = len(team_dict['Atlantic']) + len(team_dict['Southwest'])
print("屬於 Atlantic 與 Southwest 的球隊有 {} 個:".format(specific_teams_count))
print("Atlantic: {}".format(team_dict["Atlantic"]))
print("Southwest: {}".format(team_dict["Southwest"]))