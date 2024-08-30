import subprocess
import threading
import queue
import re
import argparse

def run_subfinder(domain, threads, output_queue):
    """Runs Subfinder for a given domain with specified threads and stores output in a queue."""
    cmd = f"subfinder -d {domain} -t {threads} -all -oJ"
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    for line in iter(process.stdout.readline, b''):
        decoded_line = line.decode('utf-8').strip()
        output_queue.put(decoded_line)

    process.stdout.close()
    process.wait()

def track_progress(output_queue, output_file):
    """Tracks the progress of URLs processed by Subfinder and writes to output file."""
    total_urls = 0
    processed_urls = 0
    results = []

    while True:
        try:
            output = output_queue.get(timeout=1)
            if output:
                # Example output processing: increment URL count
                if re.search(r'"host":', output):
                    total_urls += 1
                    results.append(output)
                
                processed_urls += 1

                # Print progress
                print(f"Processed URLs: {processed_urls}, Remaining: {total_urls - processed_urls}")

        except queue.Empty:
            if processed_urls == total_urls:
                print("All URLs processed.")
                break

    # Write all results to the output file
    if output_file:
        with open(output_file, "w") as file:
            file.write("\n".join(results))

def main():
    parser = argparse.ArgumentParser(description="Subfinder Progress Tracker")
    parser.add_argument("-t", "--threads", type=int, default=200, help="Number of threads for Subfinder")
    parser.add_argument("-i", "--input", type=str, required=True, help="Input file with list of domains")
    parser.add_argument("-o", "--output", type=str, help="Output file to save results")

    args = parser.parse_args()
    threads = args.threads
    input_file = args.input
    output_file = args.output

    output_queue = queue.Queue()

    with open(input_file, "r") as file:
        domains = file.read().splitlines()

    threads_list = []
    
    for domain in domains:
        subfinder_thread = threading.Thread(target=run_subfinder, args=(domain, threads, output_queue))
        threads_list.append(subfinder_thread)
        subfinder_thread.start()

    # Start tracking progress and writing to the output file
    track_progress(output_queue, output_file)

    # Wait for all Subfinder threads to finish
    for thread in threads_list:
        thread.join()

if __name__ == "__main__":
    main()
