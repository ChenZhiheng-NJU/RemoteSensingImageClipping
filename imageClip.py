# @author:Chen Zhiheng, Nanjing University
import gdal
import shapefile as shp

def saveGeoTiff(data, fileName, proj, gTran, bands, size):
    drive = gdal.GetDriverByName('GTiff')
    subImage = drive.Create(fileName, size[1], size[0], bands, gdal.GDT_UInt16)
    subImage.SetProjection(proj)
    subImage.SetGeoTransform(gTran)
    for k in range(bands):
        subImage.GetRasterBand(k + 1).WriteArray(data[k, :, :])
    subImage.FlushCache()
    subImage = None
    print('Cliping!')

def clip(img, size, proj, gTran, overlap, vectorOutputPath):
    vector = shp.Writer(vectorOutputPath)
    vector.field('Row and Columns')
    bands, row, col = img.shape
    m, n = int(row / (size[0] - overlap)), int(col / (size[1] - overlap))
    a, b, c, d, e, f = gTran

    if (m - 1) * (size[0] - overlap) + overlap < row and (n - 1) * (size[1] - overlap) + overlap < col:
        print(1)
        for i in range(m):
            for j in range(n):
                x, y = i * (size[0] - overlap), j * (size[1] - overlap)
                data = img[:, x: x + size[0], y: y + size[1]]
                saveGeoTiff(data, 'Result/{}x{}.tif'.format(i + 1, j + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
                geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
                geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
                poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
                vector.poly([poly])
                vector.record('{}x{}'.format(i + 1, j + 1))

            x, y = i * (size[0] - overlap), (col - size[1])
            data = img[:, x: x + size[0], y: y + size[1]]
            saveGeoTiff(data, 'Result/{}x{}.tif'.format(i + 1, n + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
            geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
            geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
            poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
            vector.poly([poly])
            vector.record('{}x{}'.format(i + 1, n + 1))

        for j in range(n):
            x, y = row - size[0], j * (size[1] - overlap)
            data = img[:, x: x + size[0], y: y + size[1]]
            saveGeoTiff(data, 'Result/{}x{}.tif'.format(m + 1, j + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
            geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
            geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
            poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
            vector.poly([poly])
            vector.record('{}x{}'.format(m + 1, j + 1))

        x, y = row - size[0], col - size[1]
        data = img[:, x: x + size[0], y: y + size[1]]
        saveGeoTiff(data, 'Result/{}x{}.tif'.format(m + 1, n + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
        geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
        geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
        poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
        vector.poly([poly])
        vector.record('{}x{}'.format(m + 1, n + 1))

    elif (m - 1) * (512 - overlap) + 512 < row and (n - 1) * (512 - overlap) + 512 == col:
        print(2)
        for i in range(m):
            for j in range(n):
                x, y = i * (size[0] - overlap), j * (size[1] - overlap)
                data = img[:, x: x + size[0], y: y + size[1]]
                saveGeoTiff(data, 'Result/{}x{}.tif'.format(i + 1, j + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
                geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
                geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
                poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
                vector.poly([poly])
                vector.record('{}x{}'.format(i + 1, j + 1))

        for j in range(n):
            x, y = row - size[0], j * (size[1] - overlap)
            data = img[:, x: x + size[0], y: y + size[1]]
            saveGeoTiff(data, 'Result/{}x{}.tif'.format(m + 1, j + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
            geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
            geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
            poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
            vector.poly([poly])
            vector.record('{}x{}'.format(m + 1, j + 1))

    elif (m - 1) * (512 - overlap) + 512 == row and (n - 1) * (512 - overlap) + 512 < col:
        print(3)
        for i in range(m):
            for j in range(n):
                x, y = i * (size[0] - overlap), j * (size[1] - overlap)
                data = img[:, x: x + size[0], y: y + size[1]]
                saveGeoTiff(data, 'Result/{}x{}.tif'.format(i + 1, j + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
                geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
                geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
                poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
                vector.poly([poly])
                vector.record('{}x{}'.format(i + 1, j + 1))

            x, y = i * (size[0] - overlap), (col - size[1])
            data = img[:, x: x + size[0], y: y + size[1]]
            saveGeoTiff(data, 'Result/{}x{}.tif'.format(i + 1, n + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
            geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
            geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
            poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
            vector.poly([poly])
            vector.record('{}x{}'.format(i + 1, n + 1))

    else:
        print((m - 1) * (size[0] - overlap) + size[0] , row, (n - 1) * (size[1] - overlap) + size[1] , col)
        for i in range(m):
            for j in range(n):
                x, y = i * (size[0] - overlap), j * (size[1] - overlap)
                data = img[:, x: x + size[0], y: y + size[1]]
                saveGeoTiff(data, 'Result/{}x{}.tif'.format(i + 1, j + 1), proj, (a + b * y + c * x, b, c, d + e * y + f * x, e, f), bands, size)
                geox1, geoy1 = a + b * y + c * x, d + e * y + f * x
                geox2, geoy2 = geox1 + b * (size[0]) + c * (size[1]), geoy1 + e * (size[0]) + f * (size[1])
                poly = [[geox1, geoy1], [geox2, geoy1], [geox2, geoy2], [geox1, geoy2]]
                vector.poly([poly])
                vector.record('{}x{}'.format(i + 1, j + 1))

img = gdal.Open('RasterData/研究区影像.tif')
proj = img.GetProjection()
gTran = img.GetGeoTransform()
img = img.ReadAsArray()
size = [1024, 1024]
vectorOutputPath = 'subImageCoverage.shp'
clip(img, size, proj, gTran, 128, vectorOutputPath)