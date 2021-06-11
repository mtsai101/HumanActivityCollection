import time
import numpy as np
import open3d as o3d

def main():
    frame = o3d.geometry.TriangleMesh.create_coordinate_frame(1.5)
    mesh = o3d.geometry.TriangleMesh.create_sphere()
    mesh.compute_vertex_normals()

    vis = o3d.visualization.Visualizer()
    vis.create_window(width=640, height=480)
    vis.add_geometry(frame)
    vis.add_geometry(mesh)

    ctr = vis.get_view_control()
    ctr.set_lookat([0,0,0])
    ctr.set_front([1,1,1])
    ctr.set_up([0,0,1])
    ctr.set_zoom(0.5)

    i = np.tile(np.arange(len(mesh.vertices)),(3,1)).T # (8,3)
    while True:
        # Deform mesh vertices
        vert = mesh.vertices + np.sin(i)*0.02
        mesh.vertices = o3d.utility.Vector3dVector(vert)
        i += 1

        vis.update_geometry(mesh)
        vis.update_renderer()
        vis.poll_events()

        time.sleep(0.05)
        if i[0,0]>100:
            break

    vis.run()

if __name__ == "__main__":
    main()