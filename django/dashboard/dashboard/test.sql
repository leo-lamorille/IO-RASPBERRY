SELECT AVG(humidity), AVG(temperature), AVG(airQuality)
  FROM dashboard_datas 
WHERE tStamp >= 1392730040 - 1 * 60 * 60
  AND tStamp <= 1392730040;


SELECT dashboard_datas.tStamp, ROW_NUMBER()
  FROM dashboard_datas ;