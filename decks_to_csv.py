import csv
import sys
from collections import Counter

def process_file(file_path, include_sideboard):
    single_sided = []
    double_sided = []
    sideboard_single = []
    sideboard_double = []
    process_sideboard = False
    sideboard_encountered = False
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            #print(line)
            if line.upper() == "SIDEBOARD:":
                process_sideboard = include_sideboard
                sideboard_encountered = True
                continue
            
            if not line or line.startswith('//'):
                continue  # Skip empty lines or comments
            
            quantity, card_name = line.split(' ', 1)
            quantity = int(quantity)
            card_name = card_name.split(" (")[0].replace(",", "")
            
            if '//' in card_name:
                if process_sideboard:
                    sideboard_double += [card_name] * quantity  # Changed this line
                else:
                    double_sided += [card_name] * quantity  # Changed this line
            else:
                if process_sideboard:
                    sideboard_single += [card_name] * quantity  # Changed this line
                else:
                    single_sided += [card_name] * quantity  # Changed this line
    
    return single_sided, double_sided, sideboard_single, sideboard_double, sideboard_encountered

def main(file1, file2, output_csv, include_sideboard=False):
    print(f"Sideboard processing is {'on' if include_sideboard else 'off'}.")
    
    single_sided1, double_sided1, sideboard_single1, sideboard_double1, sideboard_encountered1 = process_file(file1, include_sideboard)
    single_sided2, double_sided2, sideboard_single2, sideboard_double2, sideboard_encountered2 = process_file(file2, include_sideboard)

    if include_sideboard:
        print(f"Sideboard encountered in '{file1}': {'Yes' if sideboard_encountered1 else 'No'}.")
        print(f"Sideboard encountered in '{file2}': {'Yes' if sideboard_encountered2 else 'No'}.")

    shared_double = set(double_sided1) & set(double_sided2)
    print("All double-sided cards are shared:" if shared_double == set(double_sided1) == set(double_sided2) else "Not all double-sided cards are shared.")
    
    #convert to counter
    counter1 = Counter(single_sided1)
    counter2 = Counter(single_sided2)
    
    shared_counter = counter1 & counter2
    
    shared_single = list(shared_counter.elements())
    print("All single-sided cards are shared:" if shared_single == set(single_sided1) == set(single_sided2) else "Not all single-sided cards are shared.")  
    
    # Remove shared single-sided cards from the lists
    non_shared_counter1 = counter1 - shared_counter
    non_shared_counter2 = counter2 - shared_counter
    single_sided1 = list(non_shared_counter1.elements())
    single_sided2 = list(non_shared_counter2.elements())

    total_length1 = len(single_sided1) + len(double_sided1) + (len(sideboard_single1) + len(sideboard_double1) if include_sideboard else 0)
    total_length2 = len(single_sided2) + len(double_sided2) + (len(sideboard_single2) + len(sideboard_double2) if include_sideboard else 0)
    length_difference = abs(total_length1 - total_length2)
    print(f"Length difference between the two files: {length_difference}")

    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Quantity', 'Front', 'Back'])

        # ... (rest of the code for writing single-sided and double-sided cards)
        max_len = max(len(single_sided1), len(single_sided2))
        for i in range(max_len):
            row = ['1']
            row.append(single_sided1[i] if i < len(single_sided1) else '')
            row.append(single_sided2[i] if i < len(single_sided2) else '')
            csvwriter.writerow(row)
            
        for card in shared_single:
            csvwriter.writerow(['1', card, card])

        for card in shared_double:
            front, back = card.split(' // ')
            csvwriter.writerow(['1', front, back])

        for card in set(double_sided1) - shared_double:
            front, back = card.split(' // ')
            csvwriter.writerow(['1', front, back])

        for card in set(double_sided2) - shared_double:
            front, back = card.split(' // ')
            csvwriter.writerow(['1', front, back])
        # Append sideboard cards
        for card in sideboard_single1:
            csvwriter.writerow(['1', card, ''])
        for card in sideboard_single2:
            csvwriter.writerow(['1', '', card])
        for card in sideboard_double1:
            front, back = card.split(' // ')
            csvwriter.writerow(['1', front, back])
        for card in sideboard_double2:
            front, back = card.split(' // ')
            csvwriter.writerow(['1', front, back])

if __name__ == '__main__':
    if len(sys.argv) >= 4:
        include_sideboard = (len(sys.argv) == 5) and (sys.argv[4].lower() == 'true')
        main(sys.argv[1], sys.argv[2], sys.argv[3], include_sideboard)
    else:
        print("Usage: python script.py <input_file1.txt> <input_file2.txt> <output.csv> [<include_sideboard>]")
