import launch
import pkg_resources

onnxruntime_version = "1.14.0"
required_version = pkg_resources.parse_version(onnxruntime_version)

if not launch.is_installed("rembg"):
    launch.run_pip("install rembg==2.0.50 --no-deps", "rembg")

if launch.is_installed("onnxruntime"):
    # Get installed version
    installed_version = pkg_resources.get_distribution("onnxruntime").version
    parsed_installed_version = pkg_resources.parse_version(installed_version)

    # Uninstall onnxruntime if installed version is not the required version
    if parsed_installed_version != required_version:
        launch.run_pip(f"uninstall -y onnxruntime", "uninstall onnxruntime")

# Install the required version of onnxruntime
launch.run_pip(f"install onnxruntime=={onnxruntime_version}", f"onnxruntime {onnxruntime_version}")

for dep in ['pymatting', 'pooch']:
    if not launch.is_installed(dep):
        launch.run_pip(f"install {dep}", f"{dep} for REMBG extension")
