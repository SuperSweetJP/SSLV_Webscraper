import categoryGather
import time

all_models = [
    "https://www.ss.lv/lv/transport/cars/alfa-romeo/sell/",
    "https://www.ss.lv/lv/transport/cars/audi/sell/",
    "https://www.ss.lv/lv/transport/cars/bmw/sell/",
    "https://www.ss.lv/lv/transport/cars/cadillac/sell/",
    "https://www.ss.lv/lv/transport/cars/chevrolet/sell/",
    "https://www.ss.lv/lv/transport/cars/chrysler/sell/",
    "https://www.ss.lv/lv/transport/cars/citroen/sell/",
    "https://www.ss.lv/lv/transport/cars/dacia/sell/",
    "https://www.ss.lv/lv/transport/cars/daewoo/sell/",
    "https://www.ss.lv/lv/transport/cars/dodge/sell/",
    "https://www.ss.lv/lv/transport/cars/fiat/sell/",
    "https://www.ss.lv/lv/transport/cars/ford/sell/",
    "https://www.ss.lv/lv/transport/cars/honda/sell/",
    "https://www.ss.lv/lv/transport/cars/hyundai/sell/",
    "https://www.ss.lv/lv/transport/cars/infiniti/sell/",
    "https://www.ss.lv/lv/transport/cars/jaguar/sell/",
    "https://www.ss.lv/lv/transport/cars/jeep/sell/",
    "https://www.ss.lv/lv/transport/cars/kia/sell/",
    "https://www.ss.lv/lv/transport/cars/lancia/sell/",
    "https://www.ss.lv/lv/transport/cars/land-rover/sell/",
    "https://www.ss.lv/lv/transport/cars/lexus/sell/",
    "https://www.ss.lv/lv/transport/cars/mazda/sell/",
    "https://www.ss.lv/lv/transport/cars/mercedes/sell/",
    "https://www.ss.lv/lv/transport/cars/mini/sell/",
    "https://www.ss.lv/lv/transport/cars/mitsubishi/sell/",
    "https://www.ss.lv/lv/transport/cars/nissan/sell/",
    "https://www.ss.lv/lv/transport/cars/opel/sell/",
    "https://www.ss.lv/lv/transport/cars/peugeot/sell/",
    "https://www.ss.lv/lv/transport/cars/porsche/sell/",
    "https://www.ss.lv/lv/transport/cars/renault/sell/",
    "https://www.ss.lv/lv/transport/cars/saab/sell/",
    "https://www.ss.lv/lv/transport/cars/seat/sell/",
    "https://www.ss.lv/lv/transport/cars/skoda/sell/",
    "https://www.ss.lv/lv/transport/cars/ssangyong/sell/",
    "https://www.ss.lv/lv/transport/cars/subaru/sell/",
    "https://www.ss.lv/lv/transport/cars/suzuki/sell/",
    "https://www.ss.lv/lv/transport/cars/toyota/sell/",
    "https://www.ss.lv/lv/transport/cars/volkswagen/sell/",
    "https://www.ss.lv/lv/transport/cars/volvo/sell/",
    "https://www.ss.lv/lv/transport/cars/moskvich/sell/",
    "https://www.ss.lv/lv/transport/cars/uaz/sell/",
    "https://www.ss.lv/lv/transport/cars/gaz/sell/",
    "https://www.ss.lv/lv/transport/cars/vaz/sell/",
    "https://www.ss.lv/lv/transport/cars/others/sell/"
]

single_model = ["https://www.ss.lv/lv/transport/cars/infiniti/sell/"]



for model in single_model:
    #try:
    start_time = time.time()
    categoryGather.categoryPageLoop(model)
    run_time = time.time() - start_time
    print("category: {} completed at {} seconds".format(model, run_time))
    #except:
    #    print("issue in category: " + model)
