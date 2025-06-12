import os

gff_files_dir = "#Directory with all .gff files"
ncRNA_bedfiles_dir = "#Directory to output .bed"

# Counter for counting errors or suscessful iterations
sucess_counter = 0
error_counter = 0


for i in range(0, len(gff_files_dir)): ## My diretory was separated //
    ## .gff files from suceptible in one directory and resistant in another
    for file in os.listdir(gff_files_dir[i]): ### Goes into res or suc directory and iterate over files
        filename = file.rsplit(".", 1)[0] #Removes extension mainteining only the genome id

        output_file = f"{ncRNA_bedfiles_dir[i]}/{filename}_ncRNA.bed" #Defines output file name

        try:
            #Open the .gff file while writing a output file
            with open(f"{gff_files_dir[i]}/{file}", "r") as infile, open (output_file, "w") as outfile:
                #Iterates over each line in the .gff
                for line in infile: 
                    if line.startswith("#"):
                        continue # Jumps loop for the initial lines
                    parts = line.strip().split("\t") #Splits line by tabulation
                    if len(parts) < 9: # Avoid index errors by asserting the file has less than 9 columns
                        continue
                    if parts[2] == "misc_RNA": #ncRnas are denominated misc_RNA in column 2
                        chrom = parts[0] # Takes this information from this index in the line above
                        start = int(parts[3])
                        end = int(parts[4])
                        info = parts[8]
                        outfile.write(f"{chrom}\t{start}\t{end}\t{info}\n") # Writes a \t tabulated .bed file as required by bedtools
                    else: #Jumps loop to the next line if is not a "misc_RNA"
                        continue
        except FileExistsError: # Grabs existing files error
            error_counter += 1
            pass
        else: # Only proceds to this else if the try was suscessful
            sucess_counter += 1
print(f"{sucess_counter} files processed sucessfully!\n{error_counter} files were not processed")
print("Done!")
