import os
import xml.etree.ElementTree as ET

# 类别列表（顺序决定 class_id）
#classes = ["ore carrier", "bulk cargo carrier", "container ship", "general cargo ship", "fishing boat", "passenger ship","mixed type"]
classes = ["ship"]
def convert_annotation(xml_file, output_dir):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find("size")
    img_w = int(size.find("width").text)
    img_h = int(size.find("height").text)

    # 输出文件名
    txt_file = os.path.join(output_dir, os.path.basename(xml_file).replace(".xml", ".txt"))
    with open(txt_file, "w") as f:
        for obj in root.findall("object"):
            cls = obj.find("name").text
            cls_id = 0

            xml_box = obj.find("bndbox")
            xmin = float(xml_box.find("xmin").text)
            ymin = float(xml_box.find("ymin").text)
            xmax = float(xml_box.find("xmax").text)
            ymax = float(xml_box.find("ymax").text)

            # 转换为 YOLO 格式 (归一化)
            x_center = ((xmin + xmax) / 2.0) / img_w
            y_center = ((ymin + ymax) / 2.0) / img_h
            w = (xmax - xmin) / img_w
            h = (ymax - ymin) / img_h

            f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f}\n")

def convert_rotated_annotation(xml_file, output_dir, use_angle_degree=False):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find("size")
    img_w = int(size.find("width").text)
    img_h = int(size.find("height").text)

    # 输出文件名
    txt_file = os.path.join(output_dir, os.path.basename(xml_file).replace(".xml", ".txt"))
    with open(txt_file, "w") as f:
        for obj in root.findall("object"):
            cls = obj.find("name").text
            if cls not in classes:
                continue
            cls_id = classes.index(cls)

            rbox = obj.find("rotated_bndbox")
            cx = float(rbox.find("rotated_bbox_cx").text)
            cy = float(rbox.find("rotated_bbox_cy").text)
            w = float(rbox.find("rotated_bbox_w").text)
            h = float(rbox.find("rotated_bbox_h").text)
            theta = float(rbox.find("rotated_bbox_theta").text)  # 默认是度

            # 是否转换角度到弧度
            if not use_angle_degree:
                import math
                theta = math.radians(theta)

            # 归一化
            x_center = cx / img_w
            y_center = cy / img_h
            w = w / img_w
            h = h / img_h

            f.write(f"{cls_id} {x_center:.6f} {y_center:.6f} {w:.6f} {h:.6f} {theta:.6f}\n")


if __name__ == "__main__":
    xml_dir = r"D:\Downloads\SeaShips(7000)\Annotations"  # VOC xml文件路径
    out_dir = r"D:\Downloads\Seaships_labels"        # YOLO标签保存路径
    os.makedirs(out_dir, exist_ok=True)

    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith(".xml"):
            convert_annotation(os.path.join(xml_dir, xml_file), out_dir)

    print("转换完成！")
