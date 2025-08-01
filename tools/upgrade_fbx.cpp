#include <fbxsdk.h>
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cout << "Usage: " << argv[0] << " <input.fbx> <output.fbx>" << std::endl;
        return 1;
    }

    std::string inputFile = argv[1];
    std::string outputFile = argv[2];

    // Initialize the SDK manager
    FbxManager* sdkManager = FbxManager::Create();
    if (!sdkManager) {
        std::cout << "Error: Unable to create FBX Manager!" << std::endl;
        return 1;
    }

    // Create an IOSettings object
    FbxIOSettings* ios = FbxIOSettings::Create(sdkManager, IOSROOT);
    sdkManager->SetIOSettings(ios);

    // Create an importer
    FbxImporter* importer = FbxImporter::Create(sdkManager, "");

    // Initialize the importer
    bool importStatus = importer->Initialize(inputFile.c_str(), -1, sdkManager->GetIOSettings());
    if (!importStatus) {
        std::cout << "Error: Unable to initialize FBX importer!" << std::endl;
        std::cout << "Error returned: " << importer->GetStatus().GetErrorString() << std::endl;
        return 1;
    }

    // Create a new scene
    FbxScene* scene = FbxScene::Create(sdkManager, "");

    // Import the contents of the file into the scene
    importer->Import(scene);
    importer->Destroy();

    // Create an exporter
    FbxExporter* exporter = FbxExporter::Create(sdkManager, "");

    // Initialize the exporter
    bool exportStatus = exporter->Initialize(outputFile.c_str(), -1, sdkManager->GetIOSettings());
    if (!exportStatus) {
        std::cout << "Error: Unable to initialize FBX exporter!" << std::endl;
        std::cout << "Error returned: " << exporter->GetStatus().GetErrorString() << std::endl;
        return 1;
    }

    // Export the scene
    exporter->Export(scene);
    exporter->Destroy();

    // Destroy the SDK manager
    sdkManager->Destroy();

    std::cout << "FBX file upgraded successfully: " << inputFile << " -> " << outputFile << std::endl;
    return 0;
} 