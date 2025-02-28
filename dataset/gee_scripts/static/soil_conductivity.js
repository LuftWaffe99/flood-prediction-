var basinAssets = [
    // add your paths
  ];
  
var ksat = ee.ImageCollection("projects/sat-io/open-datasets/HiHydroSoilv2_0/ksat");
// calculate and print mean Ksat for a given basin
var calculateHydraulicConductivity = function(basinAsset) {
  var basin = ee.FeatureCollection(basinAsset);
  var basinGeometry = basin.geometry();
  var ksatImage = ksat.mean();
  var meanKsat = ksatImage.reduceRegion({
    reducer: ee.Reducer.mean(),
    geometry: basinGeometry,
    scale: 250,
    bestEffort: true, 
    maxPixels: 1e8 
  });
  // cm/day to cm/hr and scale
  var ksatMeanCmPerHr = ee.Number(meanKsat.get('b1')).divide(24000);
  return ee.Feature(null, {
    'basin_id': basinAsset,
    'soil_conductivity': ksatMeanCmPerHr
  });
};

var elevationResults = basinAssets.map(function(basinAsset) {
  return calculateHydraulicConductivity(basinAsset);
});

var elevationFeatureCollection = ee.FeatureCollection(elevationResults);

Export.table.toDrive({
  collection: elevationFeatureCollection,
  description: 'HydraulicConductivity',
  fileFormat: 'CSV',
  selectors: ['basin_id', 'soil_conductivity']
});

