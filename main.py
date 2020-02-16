spilt = "\t"
newline = "\n"


def write2file(current_id, district_name, current_pid, code):
    with open("./result.txt", "a", encoding="utf8") as r:
        r.write(current_id + spilt + district_name + spilt + str(current_pid) + spilt + code + newline)


def main():
    with open("./code.txt", "r", encoding="utf8") as origin:
        lines = origin.readlines()  # 读文件到lines
        provinces = {}  # 定义省字典
        cities = {}  # 定义市字典
        districts = {}  # 定义区字典
        for line in lines:  # 对lines循环，将省市区分开
            sp = line.split("\t")
            if sp[0][2:] == "0000":
                provinces[sp[0]] = sp[1].replace("\n", "")
                continue
            elif sp[0][4:] == "00":
                cities[sp[0]] = sp[1].replace("\n", "")
                continue
            elif sp[0][2:4] == "90" and sp[0][4:] != "00":
                cities[sp[0]] = sp[1].replace("\n", "")
                continue
            if sp[0][4:] != "00":
                districts[sp[0]] = sp[1].replace("\n", "")
                continue
        # 定义省市区的ID
        province_id = 1
        city_id = 1
        district_id = 1
        for province in provinces:
            count = 0
            for city in cities:
                if city[:2] == province[:2]:
                    count += 1
            if count == 0:
                cities[provinces[province]] = provinces[province]
        for province in provinces:  # 循环省，将省输出。
            current_id = str(province_id)
            current_pid = -1
            write2file(current_id, provinces[province], current_pid, province)
            province_cities_count = 0
            for city in cities:  # 循环市，将符合当前省的市输出
                if city[:2] == province[:2]:
                    current_id = str(city_id + len(provinces))
                    current_pid = str(province_id)
                    write2file(current_id, cities[city], current_pid, city)
                    province_cities_count += 1
                    for district in districts:  # 循环区，将符合当前市的区输出
                        if district[:4] == city[:4]:
                            current_id = str(district_id + len(cities) + len(provinces))
                            current_pid = str(city_id + len(provinces))
                            write2file(current_id, districts[district], current_pid, district)
                            district_id += 1
                    city_id += 1
            if province_cities_count == 0:  # 如果是直辖市 再输出一个市字段
                current_id = str(city_id + len(provinces))
                current_pid = str(province_id)
                write2file(current_id, provinces[province], current_pid, province)
                for district in districts:  # 循环区 将符合当前直辖市的区输出
                    if district[:2] == province[:2]:
                        current_id = str(district_id + len(cities) + len(provinces))
                        current_pid = str(city_id + +len(provinces))
                        write2file(current_id, districts[district], current_pid, district)
                        district_id += 1
                city_id += 1  # 完成市操作，ID+1
            province_id += 1  # 完成省操作，ID+1


main()