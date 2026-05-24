## Texture Feature Fusion Using LBP and GLCM for Accurate Pistachio Classification

Le-Huu-Bao Nguyen and Thi-Thu-Hong Phan

Abstract The classification of pistachio varieties is crucial to the agricultural economy, with distinct types catering to specific market demands. This reality necessitates the development of highly accurate and automated classification methods. In this chapter, we propose a novel approach that enhances pistachio classification by fusing two powerful feature extraction techniques: local binary patterns (LBP) and the gray-level co-occurrence matrix (GLCM). This combination creates a comprehensive feature representation that significantly improves classification capabilities. Experiments on a real-world dataset demonstrated the superiority of the proposed method, with a support vector machine (SVM) classifier achieving an impressive accuracy of 98.45% using the fused features. These results present significant practical implications for intelligent agricultural processing and underscore the promise of this technique for smart farming applications.

Keywords Pistachio classification · Local binary patterns · Gray-level co-occurrence matrix · Machine learning · Feature fusion

## 1 Introduction

Pistachio nuts are a high-value agricultural product widely used in the food industry due to their distinctive flavor and nutritional benefits. Varieties such as Kirmizi and Siirt exhibit unique characteristics in terms of taste, shell color, and shape, which influence consumer preferences and contribute to their varying commercial values. This natural diversity necessitates accurate varietal classification to meet market demands and ensure economic efficiency.

Traditionally, pistachio classification relies on manual sensory inspection by human experts. However, this process is subjective, labor intensive, and prone to inconsistency, especially when different varieties exhibit similar external appear-

L.-H.-B. Nguyen · T.-T.-H. Phan (

/envelopeback

)

Department of Artificial Intelligence, FPT University, Da Nang, Vietnam

e-mail: baonlhde170665@fpt.edu.vn; hongptt11@fe.edu.vn

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

ances. Such limitations not only affect product quality but may also lead to financial losses during export and distribution. Consequently, the development of automated and intelligent classification systems based on image analysis has become an essential research direction. These systems aim to improve classification accuracy, enhance quality control, and reduce human labor costs.

29

30

31

32

33

One promising approach involves integrating image processing techniques with 34 advanced machine learning (ML) algorithms to enable objective and efficient 35 quality assessment. By capturing and analyzing visual characteristics of agricultural 36 products, this approach facilitates automated inspection processes. Several studies 37 have explored this direction in the context of pistachio classification. For instance, 38 Casasent et al. [1] utilized X-ray imaging combined with a piecewise quadratic 39 neural network (PQNN) to classify pistachio nuts. Their findings demonstrated that 40 X-ray imaging holds significant potential for real-time quality inspection, achieving 41 an 88% success rate in pistachio quality classification. In another study, Omid 42 et al. [2] proposed a method that integrates image processing with machine learning 43 techniques, including artificial neural networks (ANNs) and SVM, to classify peeled 44 pistachio kernels into five color-based categories. They first segmented the images 45 and extracted 72 chromatic and four shape features from each sample. These fea46 tures were reduced to 26 using sensitivity analysis and further compressed to seven 47 via principal component analysis (PCA). Their approach achieved a classification 48 accuracy of 99.4% with ANN and 99.88% with SVM. Ozkan et al. [3] constructed a 49 dataset comprising 2148 high-resolution images of two distinct pistachio species 50 with differentiating characteristics. A computer vision system was developed to 51 classify these species through a pipeline involving image preprocessing, segmenta52 tion, extraction of 16 morphological features, and dimensionality reduction using 53 principal component analysis (PCA). The classification model, based on the k54 nearest neighbors (k-NN) algorithm, achieved an accuracy of 94.18%. 55

While traditional ML approaches have shown promising results, recent advances 56 in deep learning have opened new possibilities. In a related study, Abbaszadeh 57 et al. [4] explored an unsupervised learning approach using a deep autoencoder 58 neural network to classify pistachio nuts into two categories: problematic and 59 nonproblematic. Their method focused on detecting surface defects such as dark 60 stains, oily marks, and adhering hulls, achieving a classification accuracy of 80.3%. 61 Lisda et al. [5] proposed a deep learning-based approach utilizing convolutional 62 neural network (CNN) architectures-specifically InceptionV3 and ResNet50-to 63 classify Kirmizi and Siirt pistachio varieties. The images were preprocessed through 64 cropping and normalization before training. The InceptionV3 model achieved an 65 accuracy of 96%, outperforming ResNet50, which attained 86%. Additionally, 66 Avuclu [6] explored the use of the ResNet architecture for the same classification 67 task. Despite ResNet's well-established efficacy in general image recognition 68 problems, the best classification accuracy achieved was only 88.58%, indicating that 69 further improvements are still needed to apply deep learning methods effectively 70 in the context of agricultural image analysis. More recently, Bhuria et al. [7] 71 applied transfer learning by fine-tuning the MobileNetV2 architecture on a similarly 72 structured pistachio dataset. Their methodology included image preprocessing, 73

data augmentation, and training the network, resulting in an overall classification accuracy of 94%. Although deep learning models such as MobileNet, ResNet, and InceptionNet have demonstrated impressive performance in numerous image classification tasks, their application to pistachio classification often demands substantial computational resources. Moreover, the performance gains are not always significant compared to traditional machine learning methods, as evidenced in the study by Avuclu [6]. Therefore, there is a growing need for more efficient and resource-conserving approaches.

In response to this challenge, Nguyen and Phan [8] used a feature extraction method based on local binary patterns (LBP) to enhance classification performance. Using the same dataset as in [3], their approach was evaluated across several ML models, with the multilayer perceptron (MLP) achieving the highest accuracy of 96.74%. This impressive result, achieved solely with texture-based descriptors, underscores the crucial role of texture features in pistachio classification tasks. Inspired by these findings, this study further explores the contribution of texture descriptors to classification accuracy. Our goal is to develop a lightweight yet effective machine learning framework by combining handcrafted texture features, including local binary patterns (LBP) and gray-level co-occurrence matrix (GLCM), to enhance performance.

This chapter is organized as follows: Sect. 2 describes the methodology, Sect. 3 presents the experimental setup and results, and Sect. 4 presents conclusions with future work suggestions.

## 2 Methodology

This chapter proposes a system for the classification of pistachio varieties using image processing techniques and machine learning methods. The experimental pipeline, illustrated in Fig. 1, comprises several key stages: data preprocessing, feature extraction, model training, and performance evaluation.

Initially, the pistachio image dataset undergoes a preprocessing stage to standardize and enhance the quality of the input data. Following this, the feature extraction phase is conducted to capture discriminative information from the images. Two distinct feature extraction methods are employed concurrently: the local binary pattern (LBP) to capture local textural patterns and the gray-level co-occurrence matrix (GLCM) to analyze statistical texture features. The feature vectors obtained from both methods are then merged to create a more comprehensive feature set.

After extraction, the resulting feature dataset is partitioned into a training set (70%) and a test set (30%). In the model training stage, the training set is utilized to build and optimize various machine learning models. The models include KNN, SVM, logistic regression, random forest, extra trees, CatBoost, and a multilayer perceptron (MLP).

Finally, the performance of the trained models is evaluated using the test set. This stage aims to identify the model with the highest accuracy and best generalization

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

Fig. 1 Overview of proposed methodology

<!-- image -->

capability for the pistachio classification task. This multimodel approach allows for the selection of the most suitable and effective algorithm for the specific classification objective. The next section describes the algorithms applied in this study.

## 2.1 Feature Extraction Techniques

115

116

117

118

119

Local binary pattern (LBP) is a texture descriptor used in image processing and 120 computer vision. It is effective at capturing local intensity variations and is robust 121

against monotonic illumination changes. In this chapter, we utilize the LBP uniform patterns proposed by Ojala et al. [9]. For a standard 8-pixel neighborhood, this approach yields a 10-dimensional feature vector, which effectively represents the textural information.

The gray-level co-occurrence matrix (GLCM) introduced by Haralick et al. [10] is a method for extracting textural feature descriptors. It works by capturing the co-occurrence frequency of gray-level values within an image. In this chapter, the GLCM is computed at a distance of three pixels in four directions (0, 45, 90, and 135 degrees). Four key features-contrast, correlation, energy, and homogeneityare then calculated from each matrix. This process yields a final feature descriptor of 16 dimensions (four features × . four directions).

## 2.2 Feature Fusion

Building on previous findings where using LBP alone yielded strong classification results [8], we recognized the significant potential of local features for this task. The success of LBP indicated that detailed, localized texture information is a key differentiator for pistachios.

Therefore, this study aims to enhance performance by strategically combining complementary local descriptors while maintaining a concise feature set. We propose a novel feature fusion model that integrates LBP with the GLCM. While LBP excels at capturing fine-grained surface textures, GLCM analyzes the spatial distribution of gray levels, effectively describing broader patterns and color variations.

The fusion of these two methods results in a compact 26-dimensional vector (10 from LBP and 16 from GLCM). This combined descriptor captures a more comprehensive range of visual characteristics, compensating for the limitations of each individual method and thereby improving overall classification accuracy. This flexible methodology can be effectively applied to various image-based agricultural classification tasks.

.

<!-- formula-not-decoded -->

## 2.3 Machine Learning Models

After feature extraction, each classifier is trained to distinguish between two varieties of pistachio species. In this section, we explore several notable classification models, including:

K-nearest neighbor (KNN) is a simple, nonparametric classification method that classifies a sample based on the majority class of its K -nearest neighbors in

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

the feature space [11]. Due to its simplicity and efficiency, KNN is widely used across various domains. However, its performance is sensitive to the choice of the hyperparameter K and the distance metric used.

Support Vector Machines (SVM) is a powerful supervised learning algorithm used for both linear and nonlinear classification [12]. The core idea is to find an optimal hyperplane that maximizes the margin between the closest data points (support vectors) of different classes. For complex, nonlinear data, SVM uses the 'kernel trick' to map features into a higher-dimensional space where a linear separation is possible.

Logistic regression (LR) is a statistical algorithm that uses a logistic function to model the probability of a binary outcome from a linear combination of input features [13]. The model's coefficients are trained to maximize the likelihood of the observed data. A key advantage of LR is its interpretability, as these coefficients directly indicate the influence of each feature on the outcome's probability.

Random forest (RF) , proposed by Breiman [14], is an ensemble learning method that constructs a multitude of decision trees during training. To ensure diversity among the trees, each one is built from a different bootstrap sample of the data. Furthermore, at each node, the best split is determined from a random subset of the available features. For classification, the final prediction is decided by a majority vote among all the individual trees in the forest.

Extra trees (ET), or extremely randomized trees , is an ensemble learning algorithm that builds multiple decision trees for classification [15]. It aims to reduce model variance by introducing more randomness than random forest. This is achieved in two main ways: Each tree is trained on the entire dataset (without bootstrapping), and the split points at each node are chosen completely at random instead of being optimal. The final classification is determined by aggregating the predictions from all trees, typically through a majority vote.

CatBoost (CB) is a machine learning algorithm that leverages gradient boosting on decision trees. Unlike traditional methods that require extensive preprocessing to convert categorical features into numerical representations, this method is devoted to handling categorical features directly, eliminating the need for extensive data preprocessing. Notably, it excels at mitigating overfitting in decision trees, rendering it a robust option for classification tasks involving intricate datasets [16].

The multilayer perceptron (MLP) is a foundational class of feedforward artificial neural networks, designed to learn complex, nonlinear patterns in data [17]. Its architecture consists of an input layer, at least one hidden layer, and an output layer, with each layer being fully connected to the next. The MLP's power lies in the neurons of its hidden layers, which use nonlinear activation functions to process and transform the data. This structure enables the network to capture intricate relationships that are beyond the capabilities of simpler linear models.

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

176

177

178

179

180

181

182

183

184

185

186

187

188

189

190

191

192

193

194

195

## 3 Experiments and Results

## 3.1 Data Description

The dataset employed in this study is a publicly available collection of pistachio images originally introduced by Ozkan et al. [3]. The dataset comprises a total of 2148 images, categorized into two distinct varieties: Kirmizi (1232 images) and Siirt (916 images). These images were captured under controlled conditions using a computer vision system (CVS) to ensure quality and consistency. For the purpose of our experiments, we partitioned this dataset into a training set (70% of the images) and a testing set (30%). Sample images from both classes are presented in Fig. 2.

## 3.2 Experiments Results

This study presents an evaluation of seven classification models-KNN, SVM, LR, RF, CatBoost, ET, and MLP-for the task of distinguishing between two distinct pistachio varieties. To ensure a fair and rigorous comparison, a consistent evaluation framework was established, utilizing fixed training and testing datasets for all experiments. The effectiveness of each model was further assessed using two different feature sets. Performance was quantified using four standard metrics: accuracy (Acc), precision, recall, and the F1 score. Detailed results for each model across both feature sets are documented in Tables 2 and 3.

## (a) Performance of Individual Feature Types (LBP vs. GLCM)

The classification performance using LBP features, as reported in our previous study [8], is summarized in Table 1, while Table 2 presents the results obtained using GLCM features in the current study.

Table 1 outlines the performance of various models, all of which demonstrated strong classification ability with accuracy values above 94%. Among them, MLP

Fig. 2 Example of pistachio varieties in the dataset

<!-- image -->

196

197

198

199

200

201

202

203

204

205

206

207

208

209

210

211

212

213

214

215

216

217

218

219

| Table 1 Performance of ML methods using LBP features (%) [8]   | Model    | Precision   | Recall   | F1 score   | Accuracy   |
|----------------------------------------------------------------|----------|-------------|----------|------------|------------|
|                                                                | KNN      | 94.79       | 94.73    | 94.74      | 94.73      |
|                                                                | SVM      | 95.68       | 95.66    | 95.66      | 95.66      |
|                                                                | RF       | 95.66       | 95.66    | 95.66      | 95.66      |
|                                                                | LR       | 95.67       | 95.66    | 95.67      | 95.66      |
|                                                                | CatBoost | 96.59       | 96.59    | 96.59      | 96.59      |
|                                                                | MLP      | 96.74       | 96.74    | 96.74      | 96.74      |
| Table 2 Performance of ML methods using GLCM features (%)      | Model    | Precision   | Recall   | F1 score   | Accuracy   |
| Table 2 Performance of ML methods using GLCM features (%)      | KNN      | 86.17       | 86.20    | 86.18      | 86.20      |
|                                                                | SVM      | 89.89       | 87.91    | 87.89      | 87.91      |
|                                                                | LR       | 87.62       | 87.60    | 87.54      | 87.60      |
|                                                                | RF       | 86.65       | 86.67    | 86.65      | 87.67      |
|                                                                | ET       | 86.34       | 96.36    | 86.32      | 86.36      |
|                                                                | CatBoost | 88.34       | 88.37    | 88.34      | 88.37      |
|                                                                | MLP      | 87.90       | 87.91    | 87.89      | 87.91      |

achieved the best performance, reaching 96.74% in both accuracy and F1 score, followed closely by CatBoost at 96.59%. Traditional classifiers such as SVM, RF, and LR also yielded consistent and competitive results around 95.66%. These findings confirm that LBP features are highly effective for pistachio classification, likely due to their ability to capture local textural patterns. The strong and consistent performance across diverse ML models highlights the robustness and discriminative power of LBP features.

In contrast, the performance of GLCM features, as shown in Table 2, was generally lower across all machine learning models. The highest accuracy, 88.37%, was achieved by CatBoost, with an F1 score of 88.34%, followed closely by MLP and SVM at 87.91%. Although these results are still competitive, they consistently fall short of those obtained using LBP features. Furthermore, models such as extra trees and random forest showed larger variance in precision and recall when using GLCMfeatures, suggesting that GLCM may be more sensitive to model architecture and hyperparameters.

While LBP outperforms GLCM when used independently, the two descriptors capture complementary aspects of texture information-with LBP focusing on local micro-patterns and GLCM encoding statistical relationships over spatial regions. This motivates us to explore a fusion strategy that integrates both feature types to enhance classification performance.

## (b) Performance of Fusion Features

Table 3 presents the classification performance of various machine learning models utilizing fusion features derived from LBP and GLCM for pistachio classification.

Among all models, SVM achieved the highest accuracy of 98.45%, along with an identical F1 score, indicating excellent classification capability and a strong balance between precision and recall. Closely following, MLP also performed exceptionally

220

221

222

223

224

225

226

227

228

229

230

231

232

233

234

235

236

237

238

239

240

241

242

243

244

245

Table 3 Performance of ML methods using fusion features (%)

| Model    |   Precision |   Recall |   F1 score |   Accuracy |
|----------|-------------|----------|------------|------------|
| KNN      |       96.59 |    96.59 |      96.59 |      96.59 |
| SVM      |       98.45 |    98.44 |      98.45 |      98.45 |
| LR       |       97.06 |    97.05 |      97.05 |      97.05 |
| RF       |       96.59 |    96.59 |      96.59 |      96.59 |
| ET       |       97.36 |    97.36 |      97.36 |      97.36 |
| CatBoost |       97.98 |    97.98 |      97.98 |      97.98 |
| MLP      |       98.32 |    98.29 |      98.30 |      98.29 |

well, attaining 98.29% accuracy and an F1 score of 98.30%, reflecting its robustness and reliability in handling the classification task.

Other models, including LR (97.05%), extra trees (97.36%), CatBoost (97.98%), KNN, and random forest (both at 96.59%), also delivered highly competitive results. These findings confirm that the fusion of LBP and GLCM features provides a rich and complementary representation of texture information, leading to significant improvements in classification performance across a variety of machine learning algorithms.

## (c) Compare with Previous Study

In comparison to previous work, the current study shows a notable improvement in classification performance. Specifically, the MLP model achieved an accuracy increase of approximately 1.55%. More impressively, SVM attained the highest accuracy at 98.45%, surpassing all methods reported in the prior study. This represents a 2.79% improvement over the previous SVM result based solely on LBP features (Fig. 3) and a 1.71% gain compared to the best-performing model, MLP, in [8]. These enhancements underscore the effectiveness of combining two complementary texture descriptors: LBP, which captures fine-grained local patterns, and GLCM, which encodes regional co-occurrence statistics.

The substantial improvements observed can be attributed to the synergistic integration of LBP and GLCM features. This fusion significantly enhances the classification of pistachio varieties by leveraging the complementary strengths of each descriptor. While LBP excels at capturing fine-grained local texture patterns, GLCMencodes broader statistical relationships within spatial regions. Each feature type contributes distinct and valuable information; however, when used in isolation, they may fail to capture certain nuanced characteristics of the pistachio surface. The strategic combination of both allows one feature set to compensate for the limitations of the other, leading to a more comprehensive representation of the image. Moreover, the increased diversity introduced by integrating multiple feature types enhances the model's learning capacity, reduces the risk of overfitting, and ultimately improves generalization performance in classifying the two pistachio types.

246

247

248

249

250

251

252

253

254

255

256

257

258

259

260

261

262

263

264

265

266

267

268

269

270

271

272

273

274

275

276

Fig. 3 Comparison of ML methods using GLCM, LBP, and fusion features

<!-- image -->

## (d) Effect of Feature Types on Classification Performance

In addition to the classification results discussed above, we further examined the influence of individual feature types on the classification performance. Figure 3 shows the feature importance ranking when combining LBP and GLCM descriptors. Among the top 10 features, seven are derived from LBP, confirming its dominant role in capturing fine-grained local patterns. Nonetheless, GLCM features, such as contrast\_45 and correlation\_45, also rank highly, highlighting their contribution to capturing regional texture variations. This complementary nature underpins the superior classification performance observed, particularly with the SVM classifier (Fig. 4).

## 4 Conclusion

277

278

279

280

281

282

283

284

285

286

287

In this chapter, we investigate the effectiveness of various feature extraction 288 methods, including GLCM and LBP, for the task of classifying two pistachio 289 varieties. To leverage the strengths of each method, we propose a fusion approach 290 that effectively combines both types of features. Experimental results on a real291 world dataset demonstrate that the fused feature approach significantly outperforms 292

Fig. 4 Feature importance scores of feature fusion

<!-- image -->

individual feature sets. Notably, when utilizing the SVM classifier, an accuracy 293 of 98.45% was achieved. Based on these promising results, our future research 294 direction will focus on integrating deep learning techniques and exploring additional 295 novel feature types to further enhance the effectiveness of pistachio classification. 296

## References

1. Casasent DA, Sipe MA, Schatzki TF, Keagy PM, Lee LC (1998) Neural net classification of x-ray pistachio nut data. LWTFood Sci Technol 31(2):122-128
2. Omid M, Firouz MS, Nouri-Ahmadabadi H, Mohtasebi SS (2017) Classification of peeled pistachio kernels using computer vision and color features. Eng Agric Environ Food 10:259265
3. Ali özkan, Köklü, M, Saraço˘ glu R (2021) Classification of pistachio species using improved K-NN classifier. Progress Nutrition 23(2):2021044. https://doi.org/10.23751/pn.v23i2.9686
4. Abbaszadeh M, Rahimifard A, Eftekhari M, Zadeh HG, Fayazi A, Dini A, Danaeian M (2019) Deep learning-based classification of the defective pistachios via deep autoencoder neural networks. arXiv preprint arXiv:1906.11878. https://doi.org/10.48550/arXiv.1906.11878
5. Lisda L, Kusrini K, Ariatmanto D (2023) Classification of pistachio nut using convolutional neural network. Inform: Jurnal Ilmiah Bidang Teknologi Informasi dan Komunikasi 8(1):7177
6. Avuçlu E (2023) Classification of pistachio images with the resnet deep learning model. Selcuk J Agric Food Sci 37(2):291-300. https://doi.org/10.15316/SJAFS.2023.029

297

298

299

300

301

302

303

304

305

306

307

308

309

310

311

312

| 7. Bhuria R, Bordoloi D, Kumar BV (2024) Pistachio species classification: leveraging machine learning for quality assurance and market optimization. In: 2024 international conference on information science and communications technologies (ICISCT). IEEE, Piscataway, pp 422- 427   |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 8. Bao Nguyen LH, Phan T-T-H (2024) Local binary patterns for classifying pistachio species. In: 2024 IEEE international conference on consumer electronics-Asia (ICCE-Asia). IEEE, Piscataway, pp 1-4                                                                                   |
| 9. Ojala MP, Harwood D (1994) Performance evaluation of texture measures with classification based on Kullback discrimination of distributions. In: Proceedings of the 12th IAPR interna- tional conference on pattern recognition, vol 1, pp 582-585                                    |
| 10. Haralick RM, Shanmugam K, Dinstein I (1973) Texture analysis-segmentation using grey level co-occurrence matrix. IEEE Trans Syst Man Cybern 3(6):610-621                                                                                                                             |
| 11. Altman NS (1992) An introduction to kernel and nearest-neighbor nonparametric regression. Am Stat 46(3):175-185                                                                                                                                                                      |
| 12. Sain SR (1996) The nature of statistical learning theory. Taylor &Francis, London 13. LaValley MP (2008) Logistic regression. Circulation 117(18):2395-2399 14. Breiman L (2001) Random forests. Mach Learn 45(1):5-32                                                               |
| 15. Geurts DE, Wehenkel L (2006) Extremely randomized trees. Mach Learn 63(1):3-42                                                                                                                                                                                                       |
| Prokhorenkova L, Gusev G, Vorobev A, Dorogush AV, Gulin A (2018) CatBoost:                                                                                                                                                                                                               |
| 16. unbiased boosting with categorical features. In: Proceedings of the 32nd international conference on neural information processing systems, pp 6639-6649                                                                                                                             |
| 17. Kruse R, Mostaghim S, Borgelt C, Braune C, Steinbrecher M(2022) Multi-layer perceptrons. In: Computational intelligence: a methodological introduction. Springer, Cham, pp 53-124                                                                                                    |

313

314

315

316

317

318

319

320

321

322

323

324

325

326

327

328

329

330

331

332

333

334

335

## AUTHOR QUERIES

- AQ1. As per Springer guidelines, bold text is not allowed. Hence, it has been changed to italics for emphasis throughout the chapter. Please confirm.
- AQ2. Missing citation for 'Fig. 4' was inserted here. Please check if appropriate. Otherwise, please provide citation for 'Fig. 4'. Note that the order of main citations of figures in the text must be sequential.