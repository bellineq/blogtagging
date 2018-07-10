import sys
import csv
maxInt = sys.maxsize
decrement = True

if __name__ == '__main__':
    with open('dataset/pixnet_dataset.csv', 'r') as csvfile:
        while decrement:
            # decrease the maxInt value by factor 10 
            # as long as the OverflowError occurs.

            decrement = False
            try:
                csv.field_size_limit(maxInt)
            except OverflowError:
                maxInt = int(maxInt/10)
                decrement = True
        
        reader = csv.reader(csvfile)
        next(reader)
        techData = []
        movieData = []
        beautyData = []
        for row in reader:
            if '3c' in row[3]:
                techData.append(row)
            elif 'movie' in row[3]:
                movieData.append(row)
            elif 'beauty' in row[3]:
                beautyData.append(row)
    csvfile.close()
    
    with open('completedLinks/tech.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        completedTechLink = []
        completedTechTitle = []
        for row in reader:
            completedTechLink.append(row[0])
            completedTechTitle.append(row[1])
    csvfile.close()

    with open('completedLinks/beautymakeup.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        completedBeautyLink = []
        completedBeautyTitle = []
        for row in reader:
            completedBeautyLink.append(row[0])
            completedBeautyTitle.append(row[1])
    csvfile.close()

    with open('completedLinks/food.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        completedFoodLink = []
        completedFoodTitle = []
        for row in reader:
            completedFoodLink.append(row[0])
            completedFoodTitle.append(row[1])
    csvfile.close()

    with open('completedLinks/moviecritics.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        completedMovieLink = []
        completedMovieTitle = []
        for row in reader:
            completedMovieLink.append(row[0])
            completedMovieTitle.append(row[1])
    csvfile.close()


    with open('tech.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['url','title','content','category'])
        countT = 0
        for idx in range(len(techData)):
            countT += 1
            if techData[idx][0] not in completedTechLink and techData[idx][1] not in completedTechTitle:
                csvwriter.writerow(techData[idx])
    csvfile.close()

    with open('movie.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['url','title','content','category'])
        countM = 0
        for idx in range(len(movieData)):
            countM += 1
            if movieData[idx][0] not in completedMovieLink and movieData[idx][1] not in completedMovieTitle:
                csvwriter.writerow(movieData[idx]) 
    csvfile.close()

    with open('beauty.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['url','title','content','category'])
        countB = 0
        for idx in range(len(beautyData)):
            countB += 1
            if beautyData[idx][0] not in completedBeautyLink and beautyData[idx][1] not in completedBeautyTitle:
                csvwriter.writerow(beautyData[idx])
    csvfile.close()

    print(countT, countM, countB)