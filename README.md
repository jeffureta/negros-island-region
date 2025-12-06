# Software Development Design: Philippine Administrative Regions GeoJSON

## 1. Introduction

### 1.1 Purpose

This document outlines the design and data evolution of a repository containing GeoJSON data for the administrative regions of the Philippines. The primary purpose of this project is to provide accurate and up-to-date geospatial data for software developers, data scientists, and analysts who require Philippine administrative boundaries for mapping applications, data visualization, and regional analysis.

### 1.2 Scope

The scope of this repository is to provide two key datasets:
1.  A legacy GeoJSON file representing the 17 administrative regions of the Philippines.
2.  An updated GeoJSON file representing the 18 administrative regions, reflecting the establishment of the Negros Island Region (NIR).

The repository also includes the Python script used for this data transformation and a testing script to validate the output.

### 1.3 Overview

The administrative landscape of the Philippines was recently updated to include the Negros Island Region (NIR), increasing the total number of administrative regions from 17 to 18. This change necessitates an update to existing geospatial datasets that are used in various software applications. This repository documents this transition by providing both the legacy and updated datasets, ensuring backward compatibility while offering the most current data.

## 2. System Architecture

### 2.1 Data Files

The core of this repository consists of two GeoJSON files:

*   `ph.json`: A FeatureCollection GeoJSON file containing the polygon data for the 17 administrative regions of the Philippines. This is considered the legacy dataset.
*   `ph_updated_nir.json`: A FeatureCollection GeoJSON file containing the polygon data for the 18 administrative regions, including the newly created Negros Island Region (NIR). This is the current and recommended dataset.

### 2.2 Data Evolution

The transition from 17 to 18 regions is the central focus of this project. The `ph.json` file serves as the baseline. The `ph_updated_nir.json` is the result of a data modification process, which is programmatically handled by the scripts within this repository.

## 3. Design and Implementation

### 3.1 `ph.json` - Legacy Dataset

*   **Format:** GeoJSON FeatureCollection
*   **Content:** Contains 17 features, where each feature represents an administrative region of the Philippines prior to the creation of NIR.
*   **Coordinate System:** WGS 84 (EPSG:4326)
*   **Properties:** Each feature includes properties such as `id` and `name`.

### 3.2 `ph_updated_nir.json` - Updated Dataset

*   **Format:** GeoJSON FeatureCollection
*   **Content:** Contains 18 features. This includes all regions from `ph.json` with modifications to the Visayas regions and the addition of the Negros Island Region (NIR).
*   **Derivation:** This file is generated from `ph.json` by the `update_nir.py` script.
*   **Key Changes:**
    *   **Negros Island Region (NIR):** A new feature for NIR is created by merging the provinces of Negros Occidental (from Region VI) and Negros Oriental (from Region VII).
    *   **Region VI (Western Visayas):** Updated to exclude Negros Occidental.
    *   **Region VII (Central Visayas):** Updated to exclude Negros Oriental.
    *   **Region XVIII (Negros Island Region):** A new region feature is added.

### 3.3 `update_nir.py` - Transformation Script

This Python script is responsible for the transformation of the legacy dataset into the updated one. Its logic is as follows:
1.  Reads the `ph.json` file.
2.  Identifies the features for Western Visayas (Region VI) and Central Visayas (Region VII).
3.  Extracts the polygons corresponding to Negros Occidental and Negros Oriental.
4.  Creates a new feature for the Negros Island Region (NIR) by combining these extracted polygons.
5.  Updates the polygons for Region VI and VII to remove the respective Negros provinces.
6.  Writes the new 18-region FeatureCollection to `ph_updated_nir.json`.

### 3.4 `test_geojson.py` - Validation Script

To ensure data integrity, a test script is provided. This script performs the following checks:
1.  Validates that `ph_updated_nir.json` is a valid GeoJSON file.
2.  Confirms that the updated file contains exactly 18 features.
3.  Verifies that a feature for "Negros Island Region" exists.

## 4. Usage

Developers can utilize the GeoJSON files in this repository for various mapping and data analysis purposes.

**Example:**
To display the 18 administrative regions of the Philippines on a web map, a developer can load the `ph_updated_nir.json` file using a library like Leaflet, Mapbox, or OpenLayers.

```javascript
fetch('ph_updated_nir.json')
  .then(response => response.json())
  .then(data => {
    // L.geoJSON(data).addTo(map); // Example with Leaflet
    console.log('Loaded 18 regions:', data.features.map(f => f.properties.name));
  });
```

For projects requiring the legacy 17-region structure, `ph.json` remains available.

## 5. Future Work

*   **Province-level Data:** The dataset could be expanded to include province-level boundaries within each region.
*   **Automated Updates:** A workflow could be established to monitor official changes in Philippine administrative boundaries and automatically trigger updates to the GeoJSON files.
*   **Typings and Schemas:** Add TypeScript type definitions or JSON schemas for the properties within the GeoJSON files to improve developer experience.
