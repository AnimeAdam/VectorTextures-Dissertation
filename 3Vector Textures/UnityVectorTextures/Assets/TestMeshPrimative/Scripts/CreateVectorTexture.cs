using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[RequireComponent(typeof(MeshFilter))]
[RequireComponent(typeof(MeshRenderer))]
public class CreateVectorTexture : MonoBehaviour
{
    private MeshFilter mf;

    // Start is called before the first frame update
    void Start()
    {
        mf = GetComponent<MeshFilter>();

        //DEBUG
        DebugMeshTest();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void CreateMesh(Vector3[] vect, int[] tris, Vector2[] uvs,  Vector4[] cols)
    {
        Mesh mesh = new Mesh();

        mesh.vertices = CreateVectices(vect);
        mesh.triangles = CreateTris(tris);
        //mesh.triangles = CreateTris(vect);
        mesh.normals = CreateNormals(vect);
        mesh.uv = CreateUV(uvs);
        mesh.colors = CreateColors(vect, cols);

        mf.mesh = mesh;
    }

    #region CreateComponentsOfMesh
    
    /// <summary>
    /// Return vectices from a list of vetices produced by the vector image file
    /// </summary>
    /// <param name="vectices"></param>
    /// <returns></returns>
    Vector3[] CreateVectices(Vector3[] vectices)
    {
        Vector3[] vec3 = new Vector3[vectices.Length];

        for (int i = 0;i < vectices.Length; i++)
        {
            if (vectices[i] != null)
            {
                vec3[i] = vectices[i];
            }
            else
            {
                Debug.Log(vectices[i] + " HAS RETURNED AN NULL");
                Debug.Break();
            }
        }

        return vec3;
    }

    //int[] CreateTris(int[] tris)
    //{
    //    int[] inta = new int[tris.Length];

    //    for (int i = 0; i < tris.Length; i++)
    //    {
    //        if (tris[i] != null)
    //        {
    //            inta[i] = tris[i];
    //        }
    //        else
    //        {
    //            Debug.Log(tris[i] + " HAS RETURNED AN NULL");
    //            Debug.Break();
    //        }
    //    }

    //    return inta;
    //}

    int[] CreateTris(Vector3[] vectices)
    {
        int[] inta = new int[vectices.Length];

        if (vectices.Length % 3 != 0)
        {
            Debug.Log("VECTICES ARE NOT DIVISABLE BY THREE");
            Debug.Break();
        }

        for (int i = 0; i < vectices.Length / 3; i++)
        {
            if (vectices[i] != null)
            {
                inta[i * 3 + 0] = i + 0;
                inta[i * 3 + 1] = i + 2;
                inta[i * 3 + 2] = i + 1;
            }
            else
            {
                Debug.Log(vectices[i] + " HAS RETURNED AN NULL");
                Debug.Break();
            }
        }

        return inta;
    }

    Vector3[] CreateNormals(Vector3[] vectices)
    {
        Vector3[] vec3 = new Vector3[vectices.Length];

        for (int i = 0; i < vectices.Length; i++)
        {
            if (vectices[i] != null)                //FIX Work out normals HERE
            {
                vec3[i] = -Vector3.forward;//vectices[i];
            }
            else
            {
                Debug.Log(vectices[i] + " HAS RETURNED AN NULL");
                Debug.Break();
            }
        }

        return vec3;
    }

    Vector2[] CreateUV(Vector2[] uvs)
    {
        Vector2[] vec2 = new Vector2[uvs.Length];

        for (int i = 0; i < uvs.Length; i++)
        {
            if (uvs[i] != null)
            {
                vec2[i] = uvs[i];
            }
            else
            {
                Debug.Log(uvs[i] + " HAS RETURNED AN NULL");
                Debug.Break();
            }
        }

        return vec2;
    }

    Color[] CreateColors(Vector3[] vectices, Vector4[] cols)
    {
        Color[] col = new Color[vectices.Length];

        for (int i = 0; i < vectices.Length; i++) //FIX ADD COLOUR CONVERT TO 0f - 1f
        {
            if (vectices[i] != null)
            {
                col[i] = cols[i];
            }
            else
            {
                Debug.Log(vectices[i] + " HAS RETURNED AN NULL");
                Debug.Break();
            }
        }

        return col;
    }

    #endregion

    #region DEBUG

    void DebugMeshTest()
    {
        //Vertices
        Vector3[] vertices = new Vector3[4];
        vertices[0] = new Vector3(0, 0, 0);
        vertices[1] = new Vector3(0, 5f, 0);
        vertices[2] = new Vector3(5f, 5f, 0);
        vertices[3] = new Vector3(5f, 0, 0);

        //Triangles
        int[] tri = new int[6];
        tri[0] = 0;
        tri[1] = 1;
        tri[2] = 3;
        tri[3] = 1;
        tri[4] = 2;
        tri[5] = 3;

        //Normals



        //UVs
        Vector2[] uv = new Vector2[4];
        uv[0] = new Vector2(0, 0);
        uv[1] = new Vector2(1, 0);
        uv[2] = new Vector2(0, 1);
        uv[3] = new Vector2(1, 1);

        //Colours
        Vector4[] cols = new Vector4[vertices.Length];
        cols[0] = new Vector4(1f,0f,0f, 0f); 
        cols[1] = new Vector4(0f, 1f, 0f, 0f);
        cols[2] = new Vector4(0f, 1f, 0f, 0f);
        cols[3] = new Vector4(0f, 1f, 0f, 0f);

        CreateMesh(vertices, tri, uv, cols);
    }

    #endregion
}