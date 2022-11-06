# LANDASAT_8_9
extractlandsat.py Extract landsats files from tar extension.
renamelandsat.py This script helps users of rename the landsat image and focus on the date of the image, and save all the images names as csv file.
landsatinices.py  Calculate most of the spectral indices.
It's worthwhile that all the scripts have help in order to guid the users.  

To get the benefits of those scripts the following are the right steps.

1- rename granular using the renamelandsat.py

2- extract Landsat files from tar format extractlandsat.py

3- Landsat indices make most of the calculations landsatindices.py

"Example"

root_path = 'D:/Chapter/landsat/LC08__L2SP_169036_20150402' 

dirpath = 'D:/Chapter Elsvier/landsat/'

band4 = LandSatEightNine(root_path, 4)
band5 = LandSatEightNine(root_path, 5)

band6 = LandSatEightNine(root_path, 6)
band3 = LandSatEightNine(root_path, 3)

ndvi = NDVI(band5.band, band4.band)
output_file_ndvi = dirpath + 'ndvi_9_test.tif'
write_raster(ndvi, band4.band_crs, band4.band_transform, output_file_ndvi)
plot_plot(output_file_ndvi, 'NDVI', 'RdYlGn')



dbi = DBI(band6.band, band3.band, ndvi)
output_file_dbi = dirpath + 'dbi_9_test.tif'
write_raster(dbi, band4.band_crs, band4.band_transform, output_file_dbi)
plot_plot(output_file_dbi, 'DBI' , 'RdYlGn')

savi=SAVI(band4.band, band5.band)
output_file_savi = dirpath + 'savi.tif'
write_raster(savi, band4.band_crs, band4.band_transform, output_file_savi)
plot_plot(output_file_savi, 'SAVI' , 'cividis')


msavi2 = MSAVI2(band5.band, band4.band)
output_file_msavi2 = dirpath + 'msavi2_9_test.tif'
write_raster(msavi2, band4.band_crs, band4.band_transform, output_file_msavi2)
plot_plot(output_file_msavi2, 'MSAVI2' , 'cividis')


ndmi = NDMI(band5.band, band6.band)
output_file_ndmi = dirpath + 'ndmi_9_test.tif'
write_raster(ndmi, band4.band_crs, band4.band_transform, output_file_ndmi)
plot_plot(output_file_ndmi, 'NDMI' , 'RdYlBu')



mndwi = MNDWI(band3.band, band6.band)
output_file_mndwi = dirpath + 'mndwi_9_test.tif'
write_raster(mndwi, band3.band_crs, band3.band_transform, output_file_mndwi)
plot_plot(output_file_mndwi, 'MNDWI' , 'RdYlBu')



bai = BAI(band4.band, band5.band)
output_file_bai = dirpath + 'bai_9_test.tif'
write_raster(bai, band3.band_crs, band3.band_transform, output_file_bai)
plot_plot(output_file_bai, 'BAI' , 'PiYG')



nbri = NBRI(band5.band, band6.band)
output_file_nbri = dirpath + 'nbri_9_test.tif'
write_raster(nbri, band3.band_crs, band3.band_transform, output_file_nbri)
plot_plot(output_file_nbri, 'NBRI' , 'PiYG')




ndbi = NDBI(band6.band, band5.band, ndvi)
output_file_ndbi = dirpath + 'ndbi_9_test.tif'
write_raster(ndbi, band3.band_crs, band3.band_transform, output_file_nbri)
plot_plot(output_file_nbri, 'NBRI' , 'terrain')





B4 = normalizer(root_path, 4)
B3 = normalizer(root_path, 3)
B2 = normalizer(root_path, 2)
 


B4.plotnormalized()
B3.plotnormalized()
B2.plotnormalized()


b4 = B4.Normalizedband
b3 = B3.Normalizedband
b2 = B2.Normalizedband

color_composite(b4, b3, b2, ' Natural Color 4 3 2', cmap='terrain')

equalized_color_composite(b4, b3, b2, ' Natural Color 4 3 2', cmap='terrain')



print(band4.band_name)
print(band4.band_transform)
print(band4.raster_img)

print(band4.band_crs)
print(band4.band_shape) 
print(band4.band_profile)
