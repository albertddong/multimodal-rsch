import matplotlib.pyplot as plt

def plot_distribution(matr):
    for model_response in matr:
        plt.hist(model_response, bins=50)
        plt.show()
        
response_list = [5,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,1,5,1,1,5,5,5,3,5,5,5,5,1,5,5,5,1,1,1,1,5,1,1,4,4,1,1,1,5,1,1,1,1,5,1,1,5,1,1,1,1,1,1,1,5,1,1,1,1,1,5,5,4,1,1,5,1,1,5,1,1,1,1,1,1,1,1,3,3,3,1,1,3,5,5,1,1,5,5,5,5,5,5,5,1,5,5,5,5,1,1,1,1,1,5,1,1,5,4,5,1,]
print(len(response_list))
llava_response = response_list[::4]
cogvlm_response = response_list[1::4]
vila_response = response_list[2::4]
internvl_response = response_list[3::4]

for model in [llava_response, cogvlm_response, vila_response, internvl_response]:
    print("Extended:")
    print(model[::3])
    print(model[1::3])
    print(model[2::3])

        
#plot_distribution([llava_response, cogvlm_response, vila_response, internvl_response])