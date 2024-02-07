import struct
import trimesh

# 데이터 읽기 예시
with open('your_binary_data.bin', 'rb') as file:
    binary_data = file.read()

# struct를 사용하여 데이터 파싱
# 예시: 처음 12바이트는 XYZ 좌표를 나타내는 float32 값
num_vertices = len(binary_data) // 12  # 각 정점이 12바이트로 구성되어 있다고 가정
vertices = []
for i in range(num_vertices):
    vertex_data = binary_data[i*12:i*12+12]  # 각 정점의 바이트 슬라이스를 추출
    x, y, z = struct.unpack('fff', vertex_data)  # float32 형식으로 언패킹
    vertices.append([x, y, z])

# trimesh를 사용하여 메쉬 생성
mesh = trimesh.Trimesh(vertices=vertices)