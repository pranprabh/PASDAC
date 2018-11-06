import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os 
from datetime import datetime, timedelta
import inspect

"""
Highlight:
1. Adopt the anchor sensor scheme
2. Process by day-level continuous data block (in fact decided by watch battery life time)


Steps:

1. Anchor sensor: read in all continuous data block in day level,
  A. Put data files into groups according to continuity
  B. Read in one data block at a time according to continuity groups

2. Anchor sensor: resampling within each data block
  A. Take the first entry time of a block as start time
  B. When there is a gap in the data, if gap > 0.5 s, set value as nan, otherwise take interpolation value

3. Boat sensor: resampling anchored to anchor sensor
  A. Take the anchor sensor's time column as target time column
  B. Same as Step 2(B), when gap >0.5s, set value as nan

"""




def resample(dataDf, setting, samplingRate, gapTolerance=0, fixedTimeColumn=None, starttime=None):
    """Classifier implementing signal resampling method commonly in preprocessing stage.
    Parameters
    ----------
    dataDf : data dataframe containing unixtime column and data column(s)
    setting : setting dictionary
    samplingRate : int
        Number of samples per second
    gapTolerance: int
        if the distance between target point and either of the neighbors is further than gapTolerance in millisecond,
        then interpolation is nan
        if gapTolerance=0, the gapTolerance rule will not exist

    Examples
    --------
    >>> setting = {'TimeCol':'unixtime'}
    >>> df = pd.DataFrame(np.arange(20).reshape(5,4),
                      columns=['unixtime', 'A', 'B', 'C'])

    >>> unix = np.array([1500000000000,1500000000048,1500000000075,1500000000100,1500000000150])
    >>> df['unixtime'] = unix
    >>> print(df)
            unixtime   A   B   C
    0  1500000000000   1   2   3
    1  1500000000048   5   6   7
    2  1500000000075   9  10  11
    3  1500000000100  13  14  15
    4  1500000000150  17  18  19
    >>> newSamplingRate = 20
    >>> newDf = resample(df, setting, newSamplingRate)
    >>> print(newDf)
            unixtime          A          B          C
    0  1500000000000   1.000000   2.000000   3.000000
    1  1500000000050   5.296295   6.296295   7.296295
    2  1500000000100  13.000000  14.000000  15.000000
    3  1500000000150  17.000000  18.000000  19.000000

    >>> newSamplingRate = 33
    >>> newDf = resample(df, setting, newSamplingRate)
    >>> print(newDf)
            unixtime          A          B          C
    0  1500000000000   1.000000   2.000000   3.000000
    1  1500000000030   3.525238   4.525238   5.525238
    2  1500000000060   6.867554   7.867554   8.867554
    3  1500000000090  11.545441  12.545441  13.545441
    4  1500000000121  14.696960  15.696960  16.696960

    (Note: the 5th unixtime is 1500000000121 instead of 1500000000120, since 5th sampling is 121.21212121ms after 1st sampling.
    -----
    """

    originalNameOrder = list(dataDf.columns.values)
    # print(dataDf)

    unixtimeArr = dataDf[setting['TimeCol']].values
    deltaT = 1000.0/samplingRate
    
    dataDf = dataDf.drop(setting['TimeCol'], axis=1)
    # dataArr = dataDf.values.astype(float)
    dataArr = dataDf.values
    names = list(dataDf.columns.values)

    n = len(unixtimeArr)
    newDataList = []

    if fixedTimeColumn is None:
        #Looping through columns to apply the resampling method for each column
        for c in range(dataArr.shape[1]):
            signalArr = dataArr[:,c]

            # always include in the new signal and new time vector the first pair (time[0],singal[0])
            # if starttime == None:

            newSignalList = [signalArr[0]]
            newUnixtimeList = [unixtimeArr[0]]

            # else:
            #     newUnixtimeList = [starttime]
                # if starttime >= signalArr[0]
                # newSignalList = interpolate(unixtimeArr[tInd-1], signalArr[tInd-1], unixtimeArr[tInd], signalArr[tInd], t)

            t = unixtimeArr[0] + deltaT
            tInd = 1
            
            # check that the signal has more than one element
            if n<2:
                return

            # iterate through the original signal
            while True:
                # look for the interval that contains 't'
                i0 = tInd
                for i in range(i0,n):
                    if  t <= unixtimeArr[i]:#we found the needed time index
                        tInd = i
                        break

                # interpolate in the right interval
                if gapTolerance == 0 or \
                    ((abs(unixtimeArr[tInd-1]-t)<=gapTolerance) and \
                    (abs(unixtimeArr[tInd]-t)<=gapTolerance)):
                    s = interpolate(unixtimeArr[tInd-1], signalArr[tInd-1], \
                                    unixtimeArr[tInd], signalArr[tInd], t)
                else:
                    s = np.nan

                # apppend the new interpolated sample to the new signal and update the new time vector
                newSignalList.append(s)
                newUnixtimeList.append(int(t))

                # take step further on time
                t = t + deltaT
                
                # check the stop condition
                if t>unixtimeArr[-1]:
                    break

            newDataList.append(newSignalList)
            newDataArr = np.transpose(np.array(newDataList))

        dataDf = pd.DataFrame(data = newDataArr, columns = names)
        dataDf[setting['TimeCol']] = np.array(newUnixtimeList)

        # change to the original column order
        dataDf = dataDf[originalNameOrder]

    else:  #if fixedTimeColumn not None:
        #Looping through columns to apply the resampling method for each column
        for c in range(dataArr.shape[1]):
            signalArr = dataArr[:,c]
            newSignalList = []
            newUnixtimeList = []

            iFixedTime = 0

            t = fixedTimeColumn[iFixedTime]
            tInd = 0
            outOfRange = 1
            
            # check that the signal has more than one element
            if n<2:
                return

            # iterate through the original signal
            while True:
                # look for the interval that contains 't'
                i0 = tInd
                for i in range(i0,n):
                    if  t <= unixtimeArr[i]:#we found the needed time index
                        tInd = i
                        outOfRange = 0
                        break

                if outOfRange:
                    s = np.nan
                else:
                    # interpolate in the right interval
                    if gapTolerance == 0 or \
                        ((abs(unixtimeArr[tInd-1]-t)<=gapTolerance) and \
                        (abs(unixtimeArr[tInd]-t)<=gapTolerance)):
                        s = interpolate(unixtimeArr[tInd-1], signalArr[tInd-1], \
                                        unixtimeArr[tInd], signalArr[tInd], t)
                    elif tInd == 0: # not in above case
                        s = signalArr[tInd]
                    else:
                        s = np.nan

                # apppend the new interpolated sample to the new signal and update the new time vector
                newSignalList.append(s)
                newUnixtimeList.append(int(t))

                # check the stop condition
                if t>unixtimeArr[-1]:
                    break
                # take step further on time
                iFixedTime += 1

                if iFixedTime>=len(fixedTimeColumn):
                    break
                t = fixedTimeColumn[iFixedTime]

            newDataList.append(newSignalList)
            newDataArr = np.transpose(np.array(newDataList))

        dataDf = pd.DataFrame(data = newDataArr, columns = names)
        dataDf[setting['TimeCol']] = np.array(newUnixtimeList)

        # change to the original column order
        dataDf = dataDf[originalNameOrder]
    return dataDf


def interpolate(t1, s1, t2, s2, t):
    """Interpolates at parameter 't' between points (t1,s1) and (t2,s2)"""

    if( t1<=t and t<=t2 ): #we check if 't' is out of bounds (between t1 and t2)
        m = float(s2 - s1)/(t2 - t1)
        b = s1 - m*t1
        return m*t + b
    else:
        return np.nan



# only used in main()
def convert_filename_to_datetime(filenames):
    # NOTE: return timezone naive object
    #eg: ['08-22-17_11.csv']

    assert not isinstance(filenames, str), "Error in function: "+inspect.stack()[0][3]

    # todo: flatten the list
    dt_filenames  = []

    for filename in filenames:
        filename_split = filename.split("_")

        datestr = filename_split[0]
        hr = filename_split[1][:2]

        datetime_object = datetime.strptime(datestr, '%m-%d-%y')
        newdate = datetime_object.replace(hour=int(hr))

        dt_filenames.append(newdate)


    return dt_filenames



# only used in main()
def group_datetimes(dts):

    # assert (dts==None), "Error in function: "+inspect.stack()[0][3]

    dts.sort()
    groups = []
    subgroup = []

    subgroup.append(dts[0])
    
    for i in range(len(dts)-1):
        td = dts[i+1] - dts[i]
        if td == timedelta(hours=1):
            subgroup.append(dts[i+1])
        else:
            groups.append(subgroup)
            subgroup = [dts[i+1]]

    groups.append(subgroup)

    return groups


# only used in main()
def convert_datetime_to_filename(dt_groups):

    f_groups = []

    for dt_subgroup in dt_groups:
        f_subgroup = []

        for dt in dt_subgroup:
            f_subgroup.append(dt.strftime('%m-%d-%y_%H.csv'))

        f_groups.append(f_subgroup)

    return f_groups


# only used in main()
def group_files_by_block(filenames):
    
    dt_filenames = convert_filename_to_datetime(filenames)

    dt_groups = group_datetimes(dt_filenames)

    filename_groups = convert_datetime_to_filename(dt_groups)

    return filename_groups


def list_files_in_directory(mypath):
    return [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]


def create_folder(f, deleteExisting=False):
    '''
    Create the folder

    Parameters:
            f: folder path. Could be nested path (so nested folders will be created)

            deleteExising: if True then the existing folder will be deleted.

    '''
    if os.path.exists(f):
        if deleteExisting:
            shutil.rmtree(f)
    else:
        os.makedirs(f)




def test_case1():

    setting = {'TimeCol':'unixtime'}
    df = pd.DataFrame(np.arange(15).reshape(5,3),
                      columns=['A', 'B', 'C'])

    unix = np.array([1500000000000,1500000000048,1500000000075,1500000000349,1500000000375])
    df['unixtime'] = unix
    print('Before resampling:')
    print(df)
    print('')

    newDf = resample(df, setting, 20, gapTolerance=50)
    print('After resampling:')
    print(newDf)

    newDf = newDf.dropna(axis=0, how='any')
    print('')
    print('After dropna:')
    print(newDf)




    fixedTimeCol = newDf['unixtime'].values



    df1 = pd.DataFrame(np.arange(100,115).reshape(5,3),
                      columns=['D', 'E', 'F'])

    unix = np.array([1500000000000,1500000000047,1500000000077,1500000000300,1500000000375])
    df1['unixtime'] = unix

    print('')
    print('Before resampling:')
    print(df1)

    newDf1 = resample(df1, setting, 20, gapTolerance=50, fixedTimeColumn=fixedTimeCol)

    newDf = newDf.set_index("unixtime")
    newDf1 = newDf1.set_index("unixtime")

    newDf_concat = pd.concat([newDf,newDf1],axis=1)
 
    newDf_concat = newDf_concat.dropna(axis=0, how='any')
    
    print('After resampling:')
    print('After dropna:')
    print(newDf_concat)



def test_case2():
    # resample
    setting = {'TimeCol':'Time'}

    SENSORS = ['GYROSCOPE', 'ACCELEROMETER']

    SUBJECT = 'P121'

    newSamplingRate = 20

    for SENSOR in SENSORS:
        PATH = os.path.join('CLEAN',SUBJECT,'WRIST',SENSOR,'DATA')
        OUT_PATH = os.path.join('RESAMPLE',SUBJECT,'WRIST',SENSOR,'DATA')
        create_folder(OUT_PATH)

        files = list_files_in_directory(PATH)

        for file in files:

            if not file.startswith('.'):
                df = pd.read_csv(os.path.join(PATH, file))

                newDf = resample(df, setting, newSamplingRate)
                newDf.to_csv(os.path.join(OUT_PATH, file), index=None)





def main():

    setting = {'TimeCol':'Time'}

    newSamplingRate = 20
    gapTolerance = 500

    PATH = "/Volumes/Seagate/SHIBO/BeYourself-Structured/CLEAN"
    RESAMPLE_PATH = "/Volumes/Seagate/SHIBO/BeYourself-Structured/RESAMPLE"

    SUBJS = ['P121'] #['P108','P109','P110','P111','P112','P113','P114','P115','P116','P117','P118','P119','P121']
    DEVICE = 'WRIST'
    ANCHOR_SENSOR = 'Accelerometer'
    SENSORS = ['Gyroscope', 'Accelerometer']
    BOAT_SENSOR = 'Gyroscope'

    
    for SUBJ in SUBJS:
        anchor_folder = os.path.join(PATH, SUBJ, DEVICE, ANCHOR_SENSOR, 'DATA')
        anchor_files = list_files_in_directory(anchor_folder)
        anchor_file_groups = group_files_by_block(anchor_files)


        boat_folder = os.path.join(PATH, SUBJ, DEVICE, BOAT_SENSOR, 'DATA')

        # when Accelerometer is chosen as anchor sensor, resampled accel data will be saved besides merged acc_gyr data
        # Todo: this can be generalized to any sensor chosen as anchor sensor
        if ANCHOR_SENSOR == 'Accelerometer':
            anchor_out_folder = os.path.join(RESAMPLE_PATH, SUBJ, DEVICE, 'ACCELEROMETER', 'DATA')
        elif ANCHOR_SENSOR == 'Gyroscope':
            anchor_out_folder = os.path.join(RESAMPLE_PATH, SUBJ, DEVICE, 'GYROSCOPE', 'DATA')

        create_folder(anchor_out_folder)

        # resampled acc_gyr data will be saved
        out_folder = os.path.join(RESAMPLE_PATH, SUBJ, DEVICE, 'ACC_GYR', 'DATA')
        create_folder(out_folder)


        for group in anchor_file_groups:    
            print(group)

            # ==================================================================================
            # Anchor sensor: resampling within each data block
            # ==================================================================================

            anc_df_group = []
            for file in group:
                df = pd.read_csv(os.path.join(anchor_folder, file))
                anc_df_group.append(df)

            anc_df_concat = pd.concat(anc_df_group)
            print(len(anc_df_concat))

            anc_df_concat = anc_df_concat.sort_values(setting['TimeCol'])

            anc_df_resample = resample(anc_df_concat, setting, newSamplingRate, gapTolerance=gapTolerance)
            anc_df_resample = anc_df_resample.dropna(axis=0, how='any')

            anc_df_resample.to_csv(os.path.join(anchor_out_folder, group[0][:-4]+'_resample_gaptolerance'+str(gapTolerance)+'.csv'), index=False)

            fixedTimeCol = anc_df_resample[setting['TimeCol']].values



            # ==================================================================================
            # Boat sensor: 
            # A. Take the anchor sensor's time column as target time column
            # B. Same as Step 2(B), when gap >0.5s, set value as nan
            # ==================================================================================


            boat_df_group = []
            for file in group:
                df = pd.read_csv(os.path.join(boat_folder, file))
                boat_df_group.append(df)

            boat_df_concat = pd.concat(boat_df_group)

            boat_df_concat = boat_df_concat.sort_values(setting['TimeCol'])


            boat_df_resample = resample(boat_df_concat, setting, newSamplingRate, gapTolerance=gapTolerance, fixedTimeColumn=fixedTimeCol)

            boat_df_resample = boat_df_resample.set_index(setting['TimeCol'])
            anc_df_resample = anc_df_resample.set_index(setting['TimeCol'])


            merge_df_resample = pd.concat([anc_df_resample,boat_df_resample],axis=1)
            merge_df_resample = merge_df_resample.dropna(axis=0, how='any')

            merge_df_resample.to_csv(os.path.join(out_folder,group[0][:-4]+'_resample_gaptolerance'+str(gapTolerance)+'.csv'),index=True)



if __name__ == '__main__':

    test_case1()
    # test_case2()
    # main()
