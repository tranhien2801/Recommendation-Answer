from vncorenlp import VnCoreNLP

# To perform word segmentation, POS tagging, NER and then dependency parsing
annotator = VnCoreNLP("D:\ElcomAI\VnCoreNLP\VnCoreNLP-1.1.1.jar", annotators="wseg,pos,ner,parse", max_heap_size='-Xmx2g')

# To perform word segmentation, POS tagging and then NER
# annotator = VnCoreNLP("<FULL-PATH-to-VnCoreNLP-jar-file>", annotators="wseg,pos,ner", max_heap_size='-Xmx2g')
# To perform word segmentation and then POS tagging
# annotator = VnCoreNLP("<FULL-PATH-to-VnCoreNLP-jar-file>", annotators="wseg,pos", max_heap_size='-Xmx2g')
# To perform word segmentation only
# annotator = VnCoreNLP("<FULL-PATH-to-VnCoreNLP-jar-file>", annotators="wseg", max_heap_size='-Xmx500m')

# Input
text = "Mở đầu trang 52 Bài 15 KHTN lớp 6: Chúng ta sử dụng lương thực, thực phẩm hàng ngày để ăn uống, lấy năng lượng (nhiên liệu), dưỡng chất (nguyên liệu) cho cơ thể phát triển và hoạt động. Em có thể lựa chọn thức ăn cho mình và gia đình như thế nào để đủ chất dinh dưỡng, giúp cơ thể khỏe mạnh?"

# To perform word segmentation, POS tagging, NER and then dependency parsing
annotated_text = annotator.annotate(text)

# To perform word segmentation only
word_segmented_text = annotator.tokenize(text)

print(annotator.tokenize(text))