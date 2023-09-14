"""Demo for the retrieval_qa application."""

import os
import argparse
import pykoi

def main(**kargs):
    os.environ["DOC_PATH"] = os.path.join(os.getcwd(), "temp/docs")
    os.environ["VECTORDB_PATH"] = os.path.join(os.getcwd(), "temp/vectordb")
    MODEL_SOURCE = "openai"

    #####################################
    # Creating a retrieval QA component #
    #####################################
    # vector database
    vector_db = pykoi.VectorDbFactory.create(
        model_source=MODEL_SOURCE, vector_db_name=kargs.get("vectordb"), **kargs
    )

    # retrieval model with vector database
    retrieval_model = pykoi.RetrievalFactory.create(
        model_source=MODEL_SOURCE, vector_db=vector_db
    )

    # retrieval, chatbot, and dashboard pykoi components
    retriever = pykoi.RetrievalQA(retrieval_model=retrieval_model, vector_db=vector_db, feedback="rag")
    chatbot = pykoi.Chatbot(None, feedback="rag", is_retrieval=True)
    dashboard = pykoi.Dashboard(pykoi.RAGDatabase(), feedback="rag")

    ############################################################
    # Starting the application and retrieval qa as a component #
    ############################################################
    # Create the application
    app = pykoi.Application(debug=False, share=False)
    app.add_component(retriever)
    app.add_component(chatbot)
    app.add_component(dashboard)
    app.run()


if __name__ == "__main__":
    # Parse the command-line arguments
    parser = argparse.ArgumentParser(description="Demo for the Retrieval QA.")
    parser.add_argument(
        "-vectordb",
        type=str,
        default="chroma",
        help="Name of the vector database (default: 'chroma')",
    )
    parser.add_argument(
        "-host",
        type=str,
        default="localhost",
        help="Host address if using Epsilla vector database",
    )
    parser.add_argument(
        "-port",
        type=int,
        default=8888,
        help="Port number if using Epsilla vector database",
    )
    args = parser.parse_args()

    # Call the main function with the vector_db_name argument
    main(**vars(args))
