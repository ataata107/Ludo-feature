flag = False
safe_points = [0,8,13,21,26,34,39,47]
#First lets position the markers in a board randomly for a 1v1 match.
while(flag==False):
    points = np.random.randint(-1, high=56, size=8)
    player1_points = points[:4]
    player2_points = points[-4:]
    value =[0,0,0,0]
    for j,i in enumerate(player2_points):
        if(i<0 or i>50):
            a = 100
        else:
            a = 26 + i
        if(a>50):
            a = i- 26
        value[j] = a
    flag=True
    for i in player1_points:
        if i in value:
            if(i in safe_points):
                w =1
            else:
                flag = False
                break


#Extract the feature vector for the 4 markers which will be 45 length in total 11 for each marker plus the value of dice
feature_vector = np.zeros(45)

main_safe_points = [0,8,13,21,25,26,34,39,47]
for i in range(4):   #Iterate through player1 markers
    if (points[i] in main_safe_points):
        feature_vector[10+11*i] = 1 #At a safe point
    else:
        feature_vector[10+11*i] = 0 #Not at a safe point
    if(points[i]==-1):  # If inside assign a category
        feature_vector[11*i] = 1
        feature_vector[7+11*i] = 100 #Distance to goal is infinite
        feature_vector[8+11*i] = 100 #Distance to entry is infinite
        feature_vector[9+11*i] = 100 #Distance to next safe point is infinite
    else:
        distance_from_safe_points = main_safe_points-points[i]
        for l in (distance_from_safe_points):
            if(l>0):
                feature_vector[9+11*i] = l #Distance to next safe point 
                break
            else:
                feature_vector[9+11*i] = l #Distance from safe point 

        feature_vector[11*i] = 0
        feature_vector[7+11*i] = 56-points[i] #Distance to goal 
        feature_vector[8+11*i] = 51-points[i] #Distance to entry 
    if(points[i]==56):  #if at goal assign a category
        feature_vector[1+11*i] = 1
    else:
        feature_vector[1+11*i] = 0
    if(points[i]>50):  #If inside entry assign a category
        feature_vector[2+11*i] = 1
    else:
        feature_vector[2+11*i] = 0
    for k,j in enumerate(value):  #Iterate through opponents markers for distance purpose
        if(points[i]==-1 or points[i]>50):  #If inside or inside entry then no need to find distance
                feature_vector[3+k+11*i] = 100
                continue
        if(points[i]<25): #If player1 marker at the starting half
            if(player2_points[k]==-1 or player2_points[k]>50):  #If opponents marker inside entry or inside no need to find distance
                feature_vector[3+k+11*i] = 100
            else: 
                feature_vector[3+k+11*i] = j-points[i]
        else: #if player1s marker in the second half
            if(j<25): #if opponents marker in the first half no need to find distance
                feature_vector[3+k+11*i] = 100
            else:
                if(player2_points[k]==-1 or player2_points[k]>50): #If opponents marker inside entry or inside no need to find distance
                    feature_vector[3+k+11*i] = 100
                else:
                    feature_vector[3+k+11*i] = j-points[i]


feature_vector[-1] = random.randint(1,6)
#Now use this feature vector to train a model
