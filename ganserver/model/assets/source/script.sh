# preprocessing
# python handwritten_split_256.py handwritten_uid.jpg handwritten_uid
# python handwritten_preprocessing_256.py handwritten_uid preprocessed_uid
# python handwritten_inverse.py preprocessed_uid inversed_uid

# making training set
python ../model/assets/source/tools/src-font-image-generator.py --label-file ../model/assets/data/labels/210.txt
python ../model/assets/source/tools/trg-skeleton-image-generator.py --font-image-dir ../model/assets/data/inversed_uid --output-dir ../model/assets/data/skeleton_uid
python ../model/assets/source/tools/combine_images.py --input_dir ../model/assets/data/src-image-data/images --b_dir ../model/assets/data/inversed_uid --c_dir ../model/assets/data/skeleton_uid/images --operation combine --label-file ../model/assets/data/210.txt --output-dir ../model/assets/data/combined_uid
python ../model/assets/source/tools/images-to-tfrecords.py --image-dir ../model/assets/data/combined_uid/images --output-dir ../model/assets/data/train-tfrecords_uid

# training
python ../model/assets/source/main.py --mode train --max_epochs 1 --input_dir ../model/assets/data/train-tfrecords_uid --output_dir ../model/assets/data/trained_model_uid
# python main.py --mode train --output_dir finetuned_model_uid --max_epochs 500 --checkpoint trained_model_uid/ 

# export 2350 hangul 
python ../model/assets/source/main.py --mode test --output_dir ../model/assets/data/result_uid --checkpoint ../model/assets/data/trained_model_uid
python ../model/assets/source/split.py ../model/assets/data/result_uid