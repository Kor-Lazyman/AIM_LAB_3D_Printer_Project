import trimesh

# 3D 물체를 불러오거나 생성합니다. 여기서는 정육면체를 생성합니다.
cube = trimesh.creation.box(extents=[1, 1, 1])

# 자를 평면을 정의합니다. 여기서는 xy 평면 (z=0)으로 정의합니다.
slice_origin = [0, 0, 0]  # 평면의 원점
slice_normal = [0, 0, 1]  # 평면의 법선 벡터 (z축을 따라 수평 평면)

# 메시를 주어진 평면으로 자릅니다.
sliced_meshes = cube.slice_plane(slice_origin, slice_normal)

# 잘린 부분이 있는 경우
if isinstance(sliced_meshes, list) and len(sliced_meshes) > 0:
    print(1)
    for i, sliced_mesh in enumerate(sliced_meshes):
        # STL 파일로 저장합니다.
        sliced_mesh.export(f'sliced_part_{i}.stl')
        sliced_mesh.show()