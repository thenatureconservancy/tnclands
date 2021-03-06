# ---------------------------------------------------------------------------
# CLS_Import.py
# Created on: 2012-09-24 14:23:49.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Local variables:
SA_STEWARD_TNC_LANDS = "SA_STEWARD.TNC_LANDS"
feema1to1__2_ = "feema1to1"
SA_STEWARD_TNC_LANDS__2_ = "SA_STEWARD.TNC_LANDS"
feema1tomany__2_ = "feema1tomany"
SA_STEWARD_TNC_LANDS__3_ = "SA_STEWARD.TNC_LANDS"
feetracts__2_ = "feetracts"
SA_STEWARD_TNC_LANDS__4_ = "SA_STEWARD.TNC_LANDS"
cema1to1__2_ = "cema1to1"
SA_STEWARD_TNC_LANDS__5_ = "SA_STEWARD.TNC_LANDS"
cetr1to1__2_ = "cetr1to1"
SA_STEWARD_TNC_LANDS__6_ = "SA_STEWARD.TNC_LANDS"
cetr1tomany__2_ = "cetr1tomany"
SA_STEWARD_TNC_LANDS__7_ = "SA_STEWARD.TNC_LANDS"
rstma1to1__2_ = "rstma1to1"
SA_STEWARD_TNC_LANDS__8_ = "SA_STEWARD.TNC_LANDS"
rstma1tomany__2_ = "rstma1tomany"
SA_STEWARD_TNC_LANDS__9_ = "SA_STEWARD.TNC_LANDS"
rsttracts__2_ = "rsttracts"
cema1tomany__2_ = "cema1tomany"
SA_STEWARD_TNC_LANDS__10_ = "SA_STEWARD.TNC_LANDS"

# Process: feema1to1
arcpy.gp.Model1(SA_STEWARD_TNC_LANDS, feema1to1__2_)

# Process: feema1tomany
arcpy.gp.Model3(SA_STEWARD_TNC_LANDS__2_, feema1tomany__2_)

# Process: feetracts
arcpy.gp.feetracts(SA_STEWARD_TNC_LANDS__3_, feetracts__2_)

# Process: cema1to1
arcpy.gp.Model2(SA_STEWARD_TNC_LANDS__4_, cema1to1__2_)

# Process: cetr1to1
arcpy.gp.cetrtoma(SA_STEWARD_TNC_LANDS__5_, cetr1to1__2_)

# Process: cetr1tomany
arcpy.gp.cetrtoma2(SA_STEWARD_TNC_LANDS__6_, cetr1tomany__2_)

# Process: rstma1to1
arcpy.gp.rstma(SA_STEWARD_TNC_LANDS__7_, rstma1to1__2_)

# Process: rstma1tomany
arcpy.gp.rstma2(SA_STEWARD_TNC_LANDS__8_, rstma1tomany__2_)

# Process: rsttracts
arcpy.gp.rsttracts(SA_STEWARD_TNC_LANDS__9_, rsttracts__2_)

# Process: cema1tomany
arcpy.gp.Model4(cema1tomany__2_, SA_STEWARD_TNC_LANDS__10_)

