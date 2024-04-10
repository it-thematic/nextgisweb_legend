import { makeAutoObservable, toJS } from "mobx";

import type { FileMeta } from "@nextgisweb/file-upload/file-uploader/type";
import type { Composite } from "@nextgisweb/resource/type/Composite";
import type {
    EditorStoreOptions as EditorStoreOptionsBase,
    EditorStore as IEditorStore,
    Operation,
} from "@nextgisweb/resource/type/EditorStore";

interface Value {
    description_file?: FileMeta;
    image_file?: FileMeta;
}


export class EditorStore implements IEditorStore<Value> {
    readonly identity = "legend_style";

    description?: FileMeta = undefined;
    image?: FileMeta = undefined;

    uploading_description = false;
    uploading_image = false;

    operation?: Operation;
    composite: Composite;

    constructor({ composite, operation }: EditorStoreOptionsBase) {
        makeAutoObservable<EditorStore>(this, {
            identity: false,
            operation: false,
            composite: false,
        });
        this.operation = operation;
        this.composite = composite as Composite;
    }

    setDescription = (val?: FileMeta) => {
        this.description = val;
    };

    setImage = (val?: FileMeta) => {
        this.image = val;
    };

    setUploadingDescription = (val: boolean) => {
        this.uploading_description = val;
    };

    setUploadingImage = (val: boolean) => {
        this.uploading_image = val;
    };


    get isValid() {
        return !this.uploading_description || !this.uploading_image;
    }

    load(value: Value) {

    }

    dump() {
        const result: Value = {};
        if (this.description) {
            result.description_file = this.description;
        }
        if (this.image) {
            result.image_file = this.image;
        }
        return toJS(result);
    }
}
