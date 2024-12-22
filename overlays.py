import subprocess
import os


def list_files_in_videos_folder():
    folder_path = 'videos'
    try:
        files = os.listdir(folder_path)
        if not files:
            print(f"No files found in {folder_path}")
        else:
            print(f"Files in {folder_path}:")
            for index, file in enumerate(files, start=1):
                print(f"{index}. {file}")
            return files
    except FileNotFoundError:
        print(f"The folder {folder_path} does not exist.")
        return []


def get_component_selection():
    components = [
        'date_and_time', 'gps_info', 'gps-lock', 'big_mph', 'gradient_chart',
        'gradient', 'altitude', 'temperature', 'cadence', 'heartbeat', 'moving_map', 'journey_map'
    ]
    print("Select components to include in the overlay (default includes gps_info, gps-lock, big_mph, moving_map):")
    for index, component in enumerate(components, start=1):
        print(f"{index}. {component}")

    selected_components = input(
        "Enter the numbers of the components you want to include, separated by commas (e.g., 1,3,5): ").strip()
    if selected_components:
        selected_components = [components[int(i) - 1] for i in selected_components.split(',') if
                               i.isdigit() and 1 <= int(i) <= len(components)]
    else:
        # Default components
        selected_components = ['big_mph', 'moving_map']
        #removed these: 'gps_info', 'gps-lock',

    return selected_components


def main():
    print("GoPro Dashboard Overlay Tool")

    # List files in the videos folder
    files = list_files_in_videos_folder()

    if not files:
        return

    # Prompt user to select a file
    file_index = int(input("Enter the number of the input GoPro video file: ").strip()) - 1

    if file_index < 0 or file_index >= len(files):
        print("Invalid selection. Please run the script again.")
        return

    input_file = os.path.join('videos', files[file_index])
    output_file = os.path.join('overlayedvideos', f"{os.path.splitext(files[file_index])[0]}_overlayed.MP4")

    # Ensure the output directory exists
    os.makedirs('overlayedvideos', exist_ok=True)

    # Get include component selection
    include_components = get_component_selection()

    # Construct the command
    command = [
        'gopro-dashboard.py', '--units-speed', 'kph',
        '--gps-speed-max', '250', '--gps-speed-max-units', 'kph',
        input_file, output_file
    ]

    # Add selected components to the command
    command.extend(['--include'] + include_components)

    # Run the command
    subprocess.run(command)

    print(f"Overlays have been added successfully! Output saved to: {output_file}")


if __name__ == '__main__':
    main()
