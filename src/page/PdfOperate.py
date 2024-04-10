from .datas import FileItemData
import fitz_new


def mergeFDF(savePath: str, pdfList: list[FileItemData]):
    saveDoc = fitz_new.open()
    docList = []
    for itemData in pdfList:
        document = fitz_new.open(itemData.filePath)

        from_page = -1
        if itemData.startPos is not None:
            from_page = itemData.startPos - 1

        to_page = -1
        if itemData.endPos  is not  None:
            if itemData.endPos <= document.page_count:
                to_page = itemData.endPos - 1

        saveDoc.insert_pdf(document,from_page=from_page,to_page=to_page)
        docList.append(document)

    saveDoc.save(savePath)
    saveDoc.close()

    for doc in docList:
        doc.close()

    return True
